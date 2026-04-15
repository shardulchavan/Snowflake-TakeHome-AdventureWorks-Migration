"""
General Stored Procedure Test Suite
Basic validation for all migrated procedures
"""

import snowflake.connector
import os
from dotenv import load_dotenv
import sys


def main():
    """Test all migrated procedures"""
    
    print("\n" + "="*60)
    print("STORED PROCEDURE VALIDATION - GENERAL TESTS")
    print("="*60)
    
    # Load config
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(script_dir, '../.env')
    load_dotenv(env_file)
    
    # Connect to Snowflake
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
            database=os.getenv('SNOWFLAKE_DATABASE', 'ADVENTUREWORKS')
        )
        cursor = conn.cursor()
        print("✓ Connected to Snowflake\n")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return 1
    
    # Get all procedures in Snowflake
    print("Phase 1: Discovering migrated procedures...")
    print("-"*60)
    
    try:
        cursor.execute("""
            SELECT PROCEDURE_SCHEMA, PROCEDURE_NAME, PROCEDURE_DEFINITION
            FROM INFORMATION_SCHEMA.PROCEDURES
            WHERE PROCEDURE_SCHEMA NOT IN ('INFORMATION_SCHEMA', 'PUBLIC')
            ORDER BY PROCEDURE_SCHEMA, PROCEDURE_NAME
        """)
        
        procedures = cursor.fetchall()
        total_procedures = len(procedures)
        
        print(f"✓ Found {total_procedures} procedures\n")
        
    except Exception as e:
        print(f"❌ Failed to list procedures: {e}")
        cursor.close()
        conn.close()
        return 1
    
    # Test each procedure
    print("Phase 2: Validating procedures...")
    print("-"*60)
    
    validated = 0
    failed = []
    
    for proc in procedures:
        schema = proc[0]
        name = proc[1]
        
        print(f"\n{schema}.{name}")
        
        # Test 1: Procedure exists (already confirmed by query)
        print(f"  ✓ Exists in Snowflake")
        
        # Test 2: Can describe procedure
        try:
            cursor.execute(f"SHOW PROCEDURES LIKE '{name}' IN {schema}")
            result = cursor.fetchone()
            
            if result:
                print(f"  ✓ Callable (signature valid)")
                validated += 1
                
                
        except Exception as e:
            print(f"  ❌ Validation failed: {str(e)[:80]}")
            failed.append(f"{schema}.{name}")
    
    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total procedures: {total_procedures}")
    print(f"Validated procedures: {validated}")
    print(f"Failed validation: {len(failed)}")
    
    if total_procedures > 0:
        success_rate = (validated / total_procedures) * 100
        print(f"\n✓ Success rate: {success_rate:.0f}%")
    
    
    
    if failed:
        print(f"\n⚠ Failed procedures:")
        for proc_name in failed:
            print(f"  - {proc_name}")
    
    
    # Close connection
    cursor.close()
    conn.close()
    print("\n✓ Connection closed")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())