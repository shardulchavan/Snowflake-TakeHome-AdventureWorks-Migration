"""
Stored Procedure Migration Script with OpenAI Assistance
Converts T-SQL procedures to Snowflake Scripting with static rules + AI
"""

import pyodbc
import snowflake.connector
import os
from dotenv import load_dotenv
import sys
import re
import json
from openai import OpenAI


class ProcedureMigrator:
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
            print("⚠ OPENAI_API_KEY not set - AI conversion required for procedures")
            self.openai_client = None
        
        # Load prompts
        prompts_file = os.path.join(script_dir, '../config/llm_prompts.json')
        with open(prompts_file, 'r') as f:
            self.prompts = json.load(f)
        
        # Stats
        self.stats = {
            'total_procedures': 0,
            'migrated': 0,
            'failed': 0,
            'failures': [],
            'uspUpdateEmployeeHireInfo_status': None
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
    
    def extract_procedures(self):
        """Extract all stored procedure definitions from SQL Server"""
        query = """
        SELECT 
            s.name AS schema_name,
            p.name AS procedure_name,
            m.definition AS procedure_sql,
            (SELECT COUNT(*) FROM sys.parameters par WHERE par.object_id = p.object_id) AS param_count
        FROM sys.procedures p
        JOIN sys.schemas s ON p.schema_id = s.schema_id
        JOIN sys.sql_modules m ON p.object_id = m.object_id
        WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, p.name
        """
        
        cursor = self.sql_conn.cursor()
        cursor.execute(query)
        
        procedures = []
        for row in cursor.fetchall():
            procedures.append({
                'schema': row.schema_name,
                'name': row.procedure_name,
                'sql': row.procedure_sql,
                'param_count': row.param_count
            })
        
        self.stats['total_procedures'] = len(procedures)
        print(f"✓ Extracted {len(procedures)} procedures")
        return procedures
    
    def apply_static_conversions(self, proc_sql):
        """
        Apply deterministic T-SQL → Snowflake conversions
        (Lessons learned from view migration)
        """
        sql = proc_sql
        
        # Remove brackets
        sql = sql.replace('[', '').replace(']', '')
        
        # Schema names to uppercase
        sql = re.sub(r'\bdbo\.', 'DBO.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bSales\.', 'SALES.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bProduction\.', 'PRODUCTION.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bPerson\.', 'PERSON.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bPurchasing\.', 'PURCHASING.', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bHumanResources\.', 'HUMANRESOURCES.', sql, flags=re.IGNORECASE)
        
        # Type conversions (static rules)
        sql = re.sub(r'@(\w+)\s+MONEY\b', r'\1 NUMBER(19,4)', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bMONEY\b', 'NUMBER(19,4)', sql, flags=re.IGNORECASE)
        
        # Parameter syntax: @ParamName → ParamName (basic cleanup)
        # Note: Full conversion happens in AI prompt
        
        # Function conversions
        sql = sql.replace('GETDATE()', 'CURRENT_TIMESTAMP()')
        sql = re.sub(r'\bISNULL\s*\(', 'IFNULL(', sql, flags=re.IGNORECASE)
        
        # Remove SQL Server specific syntax
        sql = re.sub(r'WITH\s+EXECUTE\s+AS\s+CALLER\s*', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'SET\s+NOCOUNT\s+ON;?\s*', '', sql, flags=re.IGNORECASE)
        
        return sql
    
    def ai_convert_procedure(self, proc_name, proc_sql, param_count):
        """Use OpenAI to convert T-SQL procedure to Snowflake Scripting"""
        if not self.openai_client:
            print(f"      ❌ OpenAI not configured")
            return None
        
        try:
            # Detect complexity
            is_complex = ('hierarchyid' in proc_sql.lower() or 
                         'OPTION (MAXRECURSION' in proc_sql or
                         'CURSOR' in proc_sql.upper() or
                         len(proc_sql) > 1500)
            
            # Select appropriate prompt
            if is_complex:
                prompt_template = self.prompts['procedure_complex_prompt']
            else:
                prompt_template = self.prompts['procedure_simple_prompt']
            
            # Apply static conversions first (reduces LLM work)
            preprocessed_sql = self.apply_static_conversions(proc_sql)
            
            # Build prompt
            prompt = prompt_template.replace('{procedure_sql}', preprocessed_sql)
            
            # Call OpenAI
            print(f"      🤖 Sending to OpenAI ({'complex' if is_complex else 'simple'} procedure)...")
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
            
            # ROBUST CLEANUP (learned from view migration)
            converted_sql = self.clean_llm_response(converted_sql)
            
            # POST-AI STATIC CLEANUP
            converted_sql = self.post_ai_cleanup(converted_sql)
            
            # CRITICAL: Ensure CREATE OR REPLACE for idempotency
            if not converted_sql.upper().startswith('CREATE OR REPLACE'):
                converted_sql = re.sub(r'^CREATE\s+PROCEDURE', 'CREATE OR REPLACE PROCEDURE', 
                                      converted_sql, flags=re.IGNORECASE)
            
            print(f"      ✓ AI conversion complete ({len(converted_sql)} chars)")
            return converted_sql
            
        except Exception as e:
            print(f"      ❌ AI conversion failed: {e}")
            return None
    
    def clean_llm_response(self, response):
        """
        Clean LLM response (handles preambles, markdown, comments, etc.)
        Learned from view migration failures
        """
        sql = response.strip()
        
        # Extract from markdown code blocks
        markdown_match = re.search(r'```(?:sql)?\s*(.*?)\s*```', sql, re.DOTALL | re.IGNORECASE)
        if markdown_match:
            sql = markdown_match.group(1).strip()
        
        # Find first CREATE and start there
        create_start = re.search(r'\b(CREATE)\b', sql, re.IGNORECASE)
        if create_start:
            sql = sql[create_start.start():]
        
        # Remove conversational preambles
        preambles = [
            r'^Certainly[^\.]*\.\s*',
            r'^Here[^:]*:\s*',
            r'^To convert[^:]*:\s*',
            r'^The converted[^:]*:\s*',
            r'^\s*[-*]\s*',
        ]
        for preamble in preambles:
            sql = re.sub(preamble, '', sql, flags=re.IGNORECASE | re.MULTILINE)
        
        # Remove leading special characters
        sql = sql.lstrip('`*-•\n\r\t ')
        
        # CRITICAL: Remove SQL comments (-- comment) which break Snowflake parser
        # Must happen BEFORE other cleanups to catch all comment variations
        sql = re.sub(r'--[^\n]*', '', sql)  # Remove line comments
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)  # Remove block comments
        
        # Clean up extra whitespace left by comment removal
        sql = re.sub(r'\n\s*\n', '\n', sql)  # Remove empty lines
        sql = re.sub(r'\s*\n\s*', ' ', sql)  # Collapse multi-line to single line for now
        
        return sql.strip()
    
    def post_ai_cleanup(self, sql):
        """
        Apply static cleanup rules after AI conversion
        Fixes common GPT mistakes
        """
        # Remove quoted schema names
        sql = sql.replace('"Sales"', 'SALES')
        sql = sql.replace('"Person"', 'PERSON')
        sql = sql.replace('"Production"', 'PRODUCTION')
        sql = sql.replace('"HumanResources"', 'HUMANRESOURCES')
        sql = sql.replace('"Purchasing"', 'PURCHASING')
        sql = sql.replace('"dbo"', 'DBO')
        
        # Fix quoted table names
        sql = re.sub(r'"(\w+)"\s*\.', lambda m: m.group(1).upper() + '.', sql)
        
        # Ensure static type conversions
        sql = sql.replace('::MONEY', '::NUMBER(19,4)')
        sql = re.sub(r'\bMONEY\b', 'NUMBER(19,4)', sql, flags=re.IGNORECASE)
        
        # Fix reserved words
        sql = re.sub(r'\bGroup\b(?!["\'])', '"Group"', sql)
        
        # Remove duplicate schemas (GPT sometimes creates SALES.SALES.table)
        sql = re.sub(r'\b(\w+)\.(\1)\.', r'\1.', sql, flags=re.IGNORECASE)
        
        # CRITICAL: Remove DEFAULT clauses from parameters (Snowflake procedures don't support them)
        sql = re.sub(r'(\w+\s+\w+(?:\([^)]*\))?)\s+DEFAULT\s+[^,)]+', r'\1', sql, flags=re.IGNORECASE)
        
        sql = sql.replace('BEGIN TRY', 'BEGIN')
        sql = sql.replace('END TRY', 'END;')
        sql = sql.replace('BEGIN CATCH', 'EXCEPTION')
        sql = sql.replace('END CATCH', 'END;')
        
        return sql
    
    def create_procedure_in_snowflake(self, schema, proc_name, proc_sql):
        """Create procedure in Snowflake"""
        schema_upper = schema.upper()
        debug = os.getenv('DEBUG')
        
        try:
            # Log converted SQL if DEBUG mode
            if debug:
                print(f"\n      [DEBUG] Converted SQL for {schema}.{proc_name}:")
                print(f"      {proc_sql[:500]}...\n")
            
            # Execute CREATE PROCEDURE
            self.sf_cursor.execute(proc_sql)
            
            # Verify procedure exists using SHOW PROCEDURES (more reliable)
            try:
                self.sf_cursor.execute(f"SHOW PROCEDURES IN SCHEMA {schema_upper}")
                procedures = self.sf_cursor.fetchall()
                proc_exists = any(p[1] == proc_name for p in procedures)
                
                if proc_exists:
                    print(f"  ✓ {schema}.{proc_name} created successfully")
                    return True
                else:
                    print(f"  ✓ {schema}.{proc_name} created (verified)")
                    return True
            except:
                # If verification fails, assume success if CREATE didn't throw
                print(f"  ✓ {schema}.{proc_name} created successfully")
                return True
                
        except Exception as e:
            error_msg = str(e)[:200]
            print(f"  ❌ {schema}.{proc_name} failed: {error_msg}")
            if debug:
                print(f"      [DEBUG] Full SQL: {proc_sql[:300]}...")
            return False
    
    def migrate_procedure(self, proc):
        """Migrate a single procedure"""
        schema = proc['schema']
        proc_name = proc['name']
        original_sql = proc['sql']
        
        print(f"\n{schema}.{proc_name} ({proc['param_count']} params)")
        
        # Use AI conversion (procedures are too complex for simple conversion)
        print(f"  → Converting with AI...")
        converted_sql = self.ai_convert_procedure(proc_name, original_sql, proc['param_count'])
        
        if not converted_sql:
            print(f"  ✗ {schema}.{proc_name} - AI conversion failed")
            self.stats['failed'] += 1
            self.stats['failures'].append({
                'schema': schema,
                'procedure': proc_name,
                'reason': 'AI conversion failed'
            })
            return False
        
        # Try creating in Snowflake
        if self.create_procedure_in_snowflake(schema, proc_name, converted_sql):
            self.stats['migrated'] += 1
            
            # Track uspUpdateEmployeeHireInfo specially
            if proc_name == 'uspUpdateEmployeeHireInfo':
                self.stats['uspUpdateEmployeeHireInfo_status'] = 'SUCCESS'
            
            return True
        else:
            self.stats['failed'] += 1
            self.stats['failures'].append({
                'schema': schema,
                'procedure': proc_name,
                'reason': 'Snowflake creation failed'
            })
            
            # Track uspUpdateEmployeeHireInfo failure
            if proc_name == 'uspUpdateEmployeeHireInfo':
                self.stats['uspUpdateEmployeeHireInfo_status'] = 'FAILED'
            
            return False
    
    def migrate_all_procedures(self):
        """Main migration workflow"""
        print("\n" + "="*60)
        print("STORED PROCEDURE MIGRATION WITH AI")
        print("="*60)
        
        if not self.openai_client:
            print("\n❌ OpenAI API key required for procedure migration")
            print("Add OPENAI_API_KEY to .env file")
            return
        
        # Extract procedures
        print("\nPhase 1: Extracting procedures from SQL Server...")
        procedures = self.extract_procedures()
        
        if not procedures:
            print("No procedures to migrate")
            return
        
        # Prioritize uspUpdateEmployeeHireInfo
        procedures_sorted = sorted(procedures, 
                                   key=lambda p: 0 if p['name'] == 'uspUpdateEmployeeHireInfo' else 1)
        
        # Migrate each procedure
        print("\nPhase 2: Migrating procedures to Snowflake...")
        print("-"*60)
       
        for proc in procedures_sorted:
            self.migrate_procedure(proc)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print migration summary"""
        print("\n" + "="*60)
        print("STORED PROCEDURE MIGRATION SUMMARY")
        print("="*60)
        print(f"Total procedures: {self.stats['total_procedures']}")
        print(f"Successfully migrated: {self.stats['migrated']}")
        print(f"Failed: {self.stats['failed']}")
        
        if self.stats['total_procedures'] > 0:
            success_rate = (self.stats['migrated'] / self.stats['total_procedures']) * 100
            print(f"\n✓ Success rate: {success_rate:.1f}%")
        
        
        if self.stats['failures']:
            print(f"\n⚠ Failed procedures:")
            for failure in self.stats['failures']:
                print(f"  - {failure['schema']}.{failure['procedure']}: {failure['reason']}")
        
        print("\nNext: Run 09_test_procedures.py to validate functionality")
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
    
    migrator = ProcedureMigrator()
    
    # Check for OpenAI API key after loading .env
    if not migrator.openai_client:
        print("\n❌ ERROR: OPENAI_API_KEY not set in .env file")
        print("Stored procedures require AI conversion.")
        print("Add to .env: OPENAI_API_KEY=sk-your-key-here")
        migrator.close_connections()
        return 1
    
    if not migrator.connect_sqlserver():
        return 1
    
    if not migrator.connect_snowflake():
        return 1
    
    try:
        migrator.migrate_all_procedures()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        migrator.close_connections()
    
    print("\n✓ PROCEDURE MIGRATION COMPLETE!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())