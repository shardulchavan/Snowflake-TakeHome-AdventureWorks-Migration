"""
View Migration Script with OpenAI LLM Assistance
Automatically converts T-SQL views to Snowflake SQL using AI for complex cases
"""

import pyodbc
import snowflake.connector
import os
from dotenv import load_dotenv
import sys
import re
import json
from openai import OpenAI


class ViewMigratorAI:
    def __init__(self):
        """Initialize connections and OpenAI client"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(script_dir, '../.env')
        load_dotenv(env_file)
        
        # SQL Server config
        self.sql_server = os.getenv('SQL_SERVER', 'localhost,1433')
        self.sql_database = os.getenv('SQL_DATABASE', 'AdventureWorks2022')
        self.sql_username = os.getenv('SQL_USERNAME', 'sa')
        self.sql_password = os.getenv('SQL_PASSWORD')
        
        # Snowflake config
        self.sf_account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.sf_user = os.getenv('SNOWFLAKE_USER')
        self.sf_password = os.getenv('SNOWFLAKE_PASSWORD')
        self.sf_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        self.sf_database = os.getenv('SNOWFLAKE_DATABASE', 'ADVENTUREWORKS')
        
        # OpenAI config
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
            print("✓ OpenAI client initialized")
        else:
            print("⚠ OPENAI_API_KEY not set - AI conversion disabled")
            self.openai_client = None
        
        # Load prompts
        prompts_file = os.path.join(script_dir, '../config/llm_prompts.json')
        with open(prompts_file, 'r') as f:
            self.prompts = json.load(f)
        
        # Stats
        self.stats = {
            'total_views': 0,
            'created_directly': 0,
            'simple_conversion': 0,
            'ai_converted': 0,
            'failed': 0,
            'failures': []
        }
    
    def connect_sqlserver(self):
        """Connect to SQL Server"""
        try:
            conn_string = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={self.sql_server};"
                f"DATABASE={self.sql_database};"
                f"UID={self.sql_username};"
                f"PWD={self.sql_password};"
                f"TrustServerCertificate=yes;"
                f"Timeout=120;"
            )
            self.sql_conn = pyodbc.connect(conn_string, timeout=120)
            print("✓ Connected to SQL Server")
            return True
        except Exception as e:
            print(f"❌ SQL Server connection failed: {e}")
            return False
    
    def connect_snowflake(self):
        """Connect to Snowflake"""
        try:
            self.sf_conn = snowflake.connector.connect(
                user=self.sf_user,
                password=self.sf_password,
                account=self.sf_account,
                warehouse=self.sf_warehouse,
                database=self.sf_database
            )
            self.sf_cursor = self.sf_conn.cursor()
            print("✓ Connected to Snowflake")
            return True
        except Exception as e:
            print(f"❌ Snowflake connection failed: {e}")
            return False
    
    def extract_views(self):
        """Extract all view definitions from SQL Server"""
        query = """
        SELECT 
            s.name AS schema_name,
            v.name AS view_name,
            m.definition AS view_sql
        FROM sys.views v
        JOIN sys.schemas s ON v.schema_id = s.schema_id
        JOIN sys.sql_modules m ON v.object_id = m.object_id
        WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, v.name
        """
        
        cursor = self.sql_conn.cursor()
        cursor.execute(query)
        
        views = []
        for row in cursor.fetchall():
            views.append({
                'schema': row.schema_name,
                'name': row.view_name,
                'sql': row.view_sql
            })
        
        self.stats['total_views'] = len(views)
        print(f"✓ Extracted {len(views)} views")
        return views
    
    def simple_convert_view_sql(self, view_sql):
        """Simple syntax conversion (non-AI) with comprehensive static rules"""
        # Remove CREATE VIEW statement
        sql = re.sub(r'CREATE\s+VIEW\s+.*?\s+AS\s+', '', view_sql, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove brackets
        sql = sql.replace('[', '').replace(']', '')
        
        # Uppercase schema names (case-insensitive)
        sql = re.sub(r'\bdbo\.', 'DBO.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bSales\.', 'SALES.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bProduction\.', 'PRODUCTION.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bPerson\.', 'PERSON.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bPurchasing\.', 'PURCHASING.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bHumanResources\.', 'HUMANRESOURCES.', sql, flags=re.IGNORECASE)
        
        # Common function conversions
        sql = sql.replace('GETDATE()', 'CURRENT_TIMESTAMP()')
        sql = re.sub(r'\bISNULL\s*\(', 'IFNULL(', sql, flags=re.IGNORECASE)
        
        # Static type conversions
        sql = re.sub(r'\bMONEY\b', 'NUMBER(19,4)', sql, flags=re.IGNORECASE)
        sql = sql.replace('::MONEY', '::NUMBER(19,4)')
        
        # Fix year columns in PIVOT (e.g., [2002] → "2002")
        sql = re.sub(r'\b(\d{4})\b', r'"\1"', sql)
        
        # Reserved word handling
        sql = re.sub(r'\bGroup\b(?!["\'])', '"Group"', sql)  # Group → "Group" unless already quoted
        
        return sql.strip()
    
    def ai_convert_view_sql(self, view_name, view_sql):
        """Use OpenAI to convert complex view SQL"""
        if not self.openai_client:
            return None
        
        try:
            # Determine if XML view
            is_xml_view = '.value(' in view_sql or '.nodes(' in view_sql
            
            # Select appropriate prompt
            if is_xml_view:
                prompt_template = self.prompts['view_xml_specific_prompt']
            else:
                prompt_template = self.prompts['view_conversion_prompt']
            
            # Build prompt
            prompt = prompt_template.replace('{view_sql}', view_sql)
            
            # Call OpenAI
            print(f"      🤖 Sending to OpenAI for conversion...")
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.prompts['system_context']},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            converted_sql = response.choices[0].message.content.strip()
            
            # ROBUST CLEANUP - Handle all GPT response formats
            
            # Method 1: Extract from markdown code blocks
            markdown_match = re.search(r'```(?:sql)?\s*(.*?)\s*```', converted_sql, re.DOTALL | re.IGNORECASE)
            if markdown_match:
                converted_sql = markdown_match.group(1).strip()
            
            # Method 2: Remove conversational preambles (everything before SELECT/WITH/CREATE)
            sql_start = re.search(r'\b(SELECT|WITH|CREATE)\b', converted_sql, re.IGNORECASE)
            if sql_start:
                converted_sql = converted_sql[sql_start.start():]
            
            # Method 3: Remove common preamble phrases
            preambles = [
                r'^Certainly[^\.]*\.\s*',
                r'^Here[^:]*:\s*',
                r'^To convert[^:]*:\s*',
                r'^The converted[^:]*:\s*',
                r'^\s*[-*]\s*',  # Bullet points
            ]
            for preamble in preambles:
                converted_sql = re.sub(preamble, '', converted_sql, flags=re.IGNORECASE | re.MULTILINE)
            
            # Method 4: Remove any remaining leading non-SQL characters
            converted_sql = converted_sql.lstrip('`*-•\n\r\t ')
            
            # Remove CREATE VIEW if GPT added it (we only want SELECT)
            converted_sql = re.sub(r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+.*?\s+AS\s+', '', 
                                  converted_sql, flags=re.IGNORECASE | re.DOTALL)
            
            converted_sql = converted_sql.strip()
            
            print(f"      ✓ AI conversion complete ({len(converted_sql)} chars)")
            return converted_sql
            
        except Exception as e:
            print(f"      ❌ AI conversion failed: {e}")
            return None
    
    def create_view_in_snowflake(self, schema, view_name, view_sql, method="direct"):
        """
        Create view in Snowflake and test it
        
        Args:
            schema: Schema name
            view_name: View name
            view_sql: View SQL definition
            method: "direct", "simple", or "ai"
            
        Returns:
            True if successful
        """
        schema_upper = schema.upper()
        
        try:
            # Build CREATE VIEW statement
            create_sql = f"CREATE OR REPLACE VIEW {schema_upper}.{view_name} AS\n{view_sql}"
            
            # Try to create
            self.sf_cursor.execute(create_sql)
            
            # Test the view works
            self.sf_cursor.execute(f"SELECT * FROM {schema_upper}.{view_name} LIMIT 1")
            
            # Update stats based on method
            if method == "direct":
                print(f"  ✓ {schema}.{view_name} (works as-is)")
                self.stats['created_directly'] += 1
            elif method == "simple":
                print(f"  ✓ {schema}.{view_name} (simple conversion)")
                self.stats['simple_conversion'] += 1
            else:  # ai
                print(f"  ✓ {schema}.{view_name} (AI-converted)")
                self.stats['ai_converted'] += 1
            
            return True
            
        except Exception as e:
            print(f"      ❌ Failed: {str(e)[:100]}")
            return False
    
    def migrate_view(self, view):
        """
        Migrate a single view with 2-tier fallback strategy
        """
        schema = view['schema']
        view_name = view['name']
        original_sql = view['sql']
        
        print(f"\n{schema}.{view_name}")
        
        # Remove CREATE VIEW header for processing
        sql_body = re.sub(r'CREATE\s+VIEW\s+.*?\s+AS\s+', '', original_sql, 
                         flags=re.IGNORECASE | re.DOTALL).strip()
        
        # ATTEMPT 1: Try simple conversion (skip original SQL - always fails)
        print(f"  → Attempt 1: Applying simple conversions...")
        simple_converted = self.simple_convert_view_sql(original_sql)
        if self.create_view_in_snowflake(schema, view_name, simple_converted, method="simple"):
            return True
        
        # ATTEMPT 2: Use AI conversion
        if self.openai_client:
            print(f"  → Attempt 2: Using AI conversion...")
            ai_converted = self.ai_convert_view_sql(view_name, original_sql)
            
            if ai_converted:
                # POST-AI CLEANUP - Fix common GPT mistakes
                ai_converted = self.post_ai_cleanup(ai_converted)
                
                if self.create_view_in_snowflake(schema, view_name, ai_converted, method="ai"):
                    return True
        else:
            print(f"  → Attempt 2: Skipped (OpenAI not configured)")
        
        # All attempts failed
        print(f"  ✗ {schema}.{view_name} - All conversion attempts failed")
        self.stats['failed'] += 1
        self.stats['failures'].append({
            'schema': schema,
            'view': view_name,
            'reason': 'All conversion methods failed'
        })
        return False
    
    def post_ai_cleanup(self, sql):
        """
        Clean up common mistakes GPT makes + apply static conversion rules
        """
        # Remove quoted schema names that GPT adds
        sql = sql.replace('"Sales"', 'SALES')
        sql = sql.replace('"Person"', 'PERSON')
        sql = sql.replace('"Production"', 'PRODUCTION')
        sql = sql.replace('"HumanResources"', 'HUMANRESOURCES')
        sql = sql.replace('"Purchasing"', 'PURCHASING')
        sql = sql.replace('"dbo"', 'DBO')
        
        # Fix quoted table names (GPT sometimes adds these)
        sql = re.sub(r'"(\w+)"\s*\.', lambda m: m.group(1).upper() + '.', sql)
        
        # Static type conversions (deterministic, don't trust LLM)
        sql = sql.replace('::MONEY', '::NUMBER(19,4)')
        sql = re.sub(r'\bMONEY\b', 'NUMBER(19,4)', sql, flags=re.IGNORECASE)
        
        # Fix reserved word 'Group' - needs quotes when used as column alias
        sql = re.sub(r'\bGroup\b(?!["\'])', '"Group"', sql)
        
        # Ensure year columns in PIVOT remain quoted
        sql = re.sub(r'\b(\d{4})\b', r'"\1"', sql)
        
        # Fix common function variations GPT might output
        sql = re.sub(r'\bISNULL\s*\(', 'IFNULL(', sql, flags=re.IGNORECASE)
        sql = sql.replace('GETDATE()', 'CURRENT_TIMESTAMP()')
        
        # Remove any schema.schema patterns GPT creates
        sql = re.sub(r'\bSALES\.SALES\.', 'SALES.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bPERSON\.PERSON\.', 'PERSON.', sql, flags=re.IGNORECASE)
        
        return sql
    
    def migrate_all_views(self):
        """Main migration workflow"""
        print("\n" + "="*60)
        print("VIEW MIGRATION WITH AI ASSISTANCE")
        print("="*60)
        
        # Extract views
        print("\nPhase 1: Extracting view definitions from SQL Server...")
        views = self.extract_views()
        
        if not views:
            print("No views to migrate")
            return
        
        # Migrate each view
        print("\nPhase 2: Migrating views to Snowflake...")
        print("-"*60)
        
        for view in views:
            self.migrate_view(view)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print migration summary"""
        total_success = (self.stats['created_directly'] + 
                        self.stats['simple_conversion'] + 
                        self.stats['ai_converted'])
        
        print("\n" + "="*60)
        print("VIEW MIGRATION SUMMARY")
        print("="*60)
        print(f"Total views: {self.stats['total_views']}")
        print(f"\nSuccessful migrations: {total_success}/{self.stats['total_views']}")
        print(f"  - Created as-is: {self.stats['created_directly']}")
        print(f"  - Simple conversion: {self.stats['simple_conversion']}")
        print(f"  - AI-converted: {self.stats['ai_converted']}")
        print(f"\nFailed: {self.stats['failed']}")
        
        if self.stats['total_views'] > 0:
            success_rate = (total_success / self.stats['total_views']) * 100
            print(f"\n✓ Success rate: {success_rate:.1f}%")
        
        if self.stats['failures']:
            print(f"\n⚠ Failed views (require manual review):")
            for failure in self.stats['failures']:
                print(f"  - {failure['schema']}.{failure['view']}")
        
        print("="*60)
    
    def close_connections(self):
        """Close connections"""
        if hasattr(self, 'sql_conn'):
            self.sql_conn.close()
        if hasattr(self, 'sf_cursor'):
            self.sf_cursor.close()
        if hasattr(self, 'sf_conn'):
            self.sf_conn.close()
        print("\n✓ Connections closed")


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("SETUP CHECK")
    print("="*60)
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠ WARNING: OPENAI_API_KEY not set in .env file")
        print("AI-assisted conversion will be disabled.")
        print("Add to .env: OPENAI_API_KEY=your_key_here")
        print("\nContinue without AI? (y/n): ", end='')
        
        response = input().strip().lower()
        if response != 'y':
            print("Exiting. Please add OPENAI_API_KEY to .env file.")
            return 1
    
    migrator = ViewMigratorAI()
    
    if not migrator.connect_sqlserver():
        return 1
    
    if not migrator.connect_snowflake():
        return 1
    
    try:
        migrator.migrate_all_views()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        migrator.close_connections()
    
    print("\n✓ VIEW MIGRATION COMPLETE!")
    print("\nNext: Run 08_migrate_procedures_ai.py for stored procedures")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())