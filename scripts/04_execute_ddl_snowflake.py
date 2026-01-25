"""
Snowflake DDL Execution Script
Executes generated DDL files to create schema in Snowflake
"""

import snowflake.connector
import os
from dotenv import load_dotenv
import sys
from pathlib import Path


class SnowflakeDDLExecutor:
    def __init__(self):
        """Initialize Snowflake connection"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(script_dir, '../.env')
        load_dotenv(env_file)
        
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.user = os.getenv('SNOWFLAKE_USER')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        self.database = os.getenv('SNOWFLAKE_DATABASE', 'ADVENTUREWORKS')
        
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to Snowflake"""
        try:
            print("Connecting to Snowflake...")
            self.conn = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print("✓ Connected successfully\n")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def execute_sql_file(self, file_path: str, description: str):
        """Execute SQL statements from a file"""
        print(f"{'='*60}")
        print(f"Executing: {description}")
        print(f"File: {file_path}")
        print(f"{'='*60}")
        
        if not os.path.exists(file_path):
            print(f"⚠ File not found: {file_path}")
            return False
        
        # Read file
        with open(file_path, 'r') as f:
            sql_content = f.read()
        
        # Split into individual statements and clean comments
        raw_statements = sql_content.split(';')
        statements = []
        
        for stmt in raw_statements:
            # Remove comment lines and strip whitespace
            lines = stmt.split('\n')
            cleaned_lines = [line for line in lines if line.strip() and not line.strip().startswith('--')]
            cleaned_stmt = '\n'.join(cleaned_lines).strip()
            
            # Only add non-empty statements
            if cleaned_stmt:
                statements.append(cleaned_stmt)
        
        success_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements, 1):
            # Skip if statement is empty
            if not statement.strip():
                continue
            
            try:
                self.cursor.execute(statement)
                success_count += 1
                
                # Print progress every 10 statements
                if i % 10 == 0:
                    print(f"  ✓ Executed {i}/{len(statements)} statements...")
                    
            except snowflake.connector.errors.ProgrammingError as e:
                # Some errors are acceptable (e.g., object already exists)
                error_msg = str(e)
                if 'already exists' in error_msg.lower():
                    print(f"  ⚠ Statement {i}: Object already exists (skipping)")
                    success_count += 1
                else:
                    print(f"  ❌ Statement {i} failed: {error_msg}")
                    error_count += 1
            except Exception as e:
                print(f"  ❌ Statement {i} failed: {e}")
                error_count += 1
        
        print(f"\n✓ Completed: {success_count} successful, {error_count} errors")
        print()
        return error_count == 0
    
    def verify_schema_creation(self):
        """Verify schemas were created"""
        print(f"{'='*60}")
        print("Verifying Schema Creation")
        print(f"{'='*60}")
        
        self.cursor.execute("SHOW SCHEMAS")
        schemas = [row[1] for row in self.cursor.fetchall()]
        
        custom_schemas = [s for s in schemas if s not in ['INFORMATION_SCHEMA', 'PUBLIC']]
        
        if custom_schemas:
            print(f"✓ Found {len(custom_schemas)} custom schemas:")
            for schema in custom_schemas:
                print(f"  - {schema}")
        else:
            print("⚠ No custom schemas found")
        
        print()
        return len(custom_schemas) > 0
    
    def verify_tables_creation(self):
        """Verify tables were created"""
        print(f"{'='*60}")
        print("Verifying Table Creation")
        print(f"{'='*60}")
        
        # Get all schemas except system ones
        self.cursor.execute("SHOW SCHEMAS")
        schemas = [row[1] for row in self.cursor.fetchall() 
                  if row[1] not in ['INFORMATION_SCHEMA', 'PUBLIC']]
        
        total_tables = 0
        schema_table_counts = {}
        
        for schema in schemas:
            # Snowflake automatically uppercase unquoted identifiers
            self.cursor.execute(f"SHOW TABLES IN SCHEMA {schema}")
            tables = self.cursor.fetchall()
            count = len(tables)
            schema_table_counts[schema] = count
            total_tables += count
        
        print(f"✓ Total tables created: {total_tables}")
        for schema, count in sorted(schema_table_counts.items()):
            print(f"  - {schema}: {count} tables")
        
        print()
        return total_tables > 0
    
    def verify_sequences_creation(self):
        """Verify sequences were created"""
        print(f"{'='*60}")
        print("Verifying Sequence Creation")
        print(f"{'='*60}")
        
        self.cursor.execute("SHOW SEQUENCES")
        sequences = self.cursor.fetchall()
        
        if sequences:
            print(f"✓ Created {len(sequences)} sequences for identity columns")
            # Show first 5 as examples
            for seq in sequences[:5]:
                print(f"  - {seq[1]}.{seq[0]}")
            if len(sequences) > 5:
                print(f"  ... and {len(sequences) - 5} more")
        else:
            print("⚠ No sequences found")
        
        print()
        return True
    
    def get_sample_data_query(self):
        """Return sample queries to test schema"""
        return """
-- Sample queries to test your new Snowflake schema:

-- 1. Check all schemas
SHOW SCHEMAS;

-- 2. Check tables in Sales schema
SHOW TABLES IN SALES;

-- 3. View table structure
DESCRIBE TABLE SALES.CUSTOMER;

-- 4. Check row counts (will be 0 until data migration)
SELECT 'Sales.Customer' as table_name, COUNT(*) as row_count FROM SALES.CUSTOMER
UNION ALL
SELECT 'Production.Product', COUNT(*) FROM PRODUCTION.PRODUCT
UNION ALL
SELECT 'Person.Person', COUNT(*) FROM PERSON.PERSON;
"""
    
    def close(self):
        """Close Snowflake connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✓ Connection closed")


def main():
    print("\n" + "="*60)
    print("SNOWFLAKE DDL EXECUTION")
    print("="*60)
    print()
    
    # Get script directory for absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ddl_dir = os.path.join(script_dir, '../snowflake_ddl')
    
    # DDL files to execute in order
    ddl_files = [
        (os.path.join(ddl_dir, '01_schemas.sql'), 'Creating Schemas'),
        (os.path.join(ddl_dir, '02_sequences.sql'), 'Creating Sequences'),
        (os.path.join(ddl_dir, '03_tables.sql'), 'Creating Tables'),
        (os.path.join(ddl_dir, '04_primary_keys.sql'), 'Adding Primary Keys'),
        (os.path.join(ddl_dir, '05_foreign_keys.sql'), 'Adding Foreign Keys'),
    ]
    
    # Initialize executor
    executor = SnowflakeDDLExecutor()
    
    # Connect
    if not executor.connect():
        return 1
    
    # Execute DDL files
    all_success = True
    for file_path, description in ddl_files:
        if os.path.exists(file_path):
            success = executor.execute_sql_file(file_path, description)
            if not success:
                all_success = False
                print(f"⚠ Warning: Some errors occurred in {file_path}")
        else:
            print(f"⚠ Skipping {file_path} - file not found")
    
    print()
    
    # Verify creation
    executor.verify_schema_creation()
    executor.verify_tables_creation()
    executor.verify_sequences_creation()
    
    # Print summary
    print("="*60)
    if all_success:
        print("✓ DDL EXECUTION COMPLETE")
        print("="*60)
        print("\nYour Snowflake schema is ready!")
        print("Tables are created but empty (0 rows)")
        print("\nNext steps:")
        print("  1. Review schema in Snowflake UI")
        print("  2. Run data migration (Phase 4)")
        print("\n" + executor.get_sample_data_query())
    else:
        print("⚠ DDL EXECUTION COMPLETED WITH WARNINGS")
        print("="*60)
        print("\nSome statements had errors, but this may be normal")
        print("(e.g., objects already existing)")
        print("Review the output above for details")
    
    print("="*60)
    
    # Close connection
    executor.close()
    
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())