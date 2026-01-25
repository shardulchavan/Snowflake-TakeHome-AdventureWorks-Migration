"""
Snowflake Connection Test Script
Tests connectivity and validates Snowflake environment setup
"""

import snowflake.connector
import os
from dotenv import load_dotenv
import sys


def test_snowflake_connection():
    """Test Snowflake connection and environment"""
    
    print("\n=== Snowflake Connection Test ===\n")
    
    # Load environment variables
    load_dotenv('../.env')
    
    # Get credentials
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    user = os.getenv('SNOWFLAKE_USER')
    password = os.getenv('SNOWFLAKE_PASSWORD')
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
    database = os.getenv('SNOWFLAKE_DATABASE', 'ADVENTUREWORKS')
    
    # Validate credentials exist
    if not all([account, user, password]):
        print("❌ ERROR: Missing Snowflake credentials in .env file")
        print("\nRequired variables:")
        print("  - SNOWFLAKE_ACCOUNT")
        print("  - SNOWFLAKE_USER")
        print("  - SNOWFLAKE_PASSWORD")
        return False
    
    print(f"Account: {account}")
    print(f"User: {user}")
    print(f"Warehouse: {warehouse}")
    print(f"Database: {database}")
    print()
    
    try:
        # Test connection
        print("Step 1: Testing connection...")
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        )
        cursor = conn.cursor()
        print("✓ Connection successful")
        
        # Test warehouse
        print("\nStep 2: Testing warehouse...")
        cursor.execute(f"USE WAREHOUSE {warehouse}")
        cursor.execute("SELECT CURRENT_WAREHOUSE()")
        result = cursor.fetchone()
        print(f"✓ Warehouse active: {result[0]}")
        
        # Check if database exists
        print("\nStep 3: Checking database...")
        cursor.execute("SHOW DATABASES")
        databases = [row[1] for row in cursor.fetchall()]
        
        if database in databases:
            print(f"✓ Database exists: {database}")
            cursor.execute(f"USE DATABASE {database}")
        else:
            print(f"⚠ Database not found: {database}")
            print(f"  Creating database...")
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"✓ Database created: {database}")
        
        # List existing schemas
        print("\nStep 4: Checking schemas...")
        cursor.execute("SHOW SCHEMAS")
        schemas = [row[1] for row in cursor.fetchall()]
        
        if len(schemas) > 2:  # More than just INFORMATION_SCHEMA and PUBLIC
            print(f"✓ Found {len(schemas)} schemas:")
            for schema in schemas:
                if schema not in ['INFORMATION_SCHEMA', 'PUBLIC']:
                    print(f"  - {schema}")
        else:
            print("⚠ No custom schemas found (will be created during migration)")
        
        # Get account info
        print("\nStep 5: Account information...")
        cursor.execute("SELECT CURRENT_ACCOUNT(), CURRENT_REGION()")
        account_info = cursor.fetchone()
        print(f"✓ Account: {account_info[0]}")
        print(f"✓ Region: {account_info[1]}")
        
        # Check warehouse size
        print("\nStep 6: Warehouse configuration...")
        cursor.execute(f"SHOW WAREHOUSES LIKE '{warehouse}'")
        wh_info = cursor.fetchone()
        if wh_info:
            print(f"✓ Size: {wh_info[3]}")
            print(f"✓ State: {wh_info[2]}")
        
        # Test query execution
        print("\nStep 7: Testing query execution...")
        cursor.execute("SELECT 'Hello from Snowflake!' as message")
        result = cursor.fetchone()
        print(f"✓ Query test: {result[0]}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED")
        print("="*50)
        print("\nYour Snowflake environment is ready!")
        print("You can proceed with schema creation and data migration.")
        print("="*50)
        
        return True
        
    except snowflake.connector.errors.ProgrammingError as e:
        print(f"\n❌ Snowflake Error: {e}")
        print("\nCommon issues:")
        print("  - Check account identifier format (should be: account.region)")
        print("  - Verify username and password")
        print("  - Ensure warehouse exists and is running")
        return False
        
    except snowflake.connector.errors.DatabaseError as e:
        print(f"\n❌ Database Error: {e}")
        print("\nCheck:")
        print("  - Network connectivity")
        print("  - Firewall settings")
        print("  - Account is active (not suspended)")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False


def print_setup_instructions():
    """Print setup instructions if test fails"""
    print("\n" + "="*50)
    print("SNOWFLAKE SETUP CHECKLIST")
    print("="*50)
    print("\n1. Create Snowflake account:")
    print("   https://signup.snowflake.com/")
    print("\n2. Note your account identifier:")
    print("   Format: <account>.<region>")
    print("   Example: abc12345.us-east-1")
    print("\n3. Create warehouse (in Snowflake UI):")
    print("   CREATE WAREHOUSE COMPUTE_WH")
    print("   WAREHOUSE_SIZE = 'XSMALL'")
    print("   AUTO_SUSPEND = 60;")
    print("\n4. Update .env file with credentials:")
    print("   SNOWFLAKE_ACCOUNT=your_account.region")
    print("   SNOWFLAKE_USER=your_username")
    print("   SNOWFLAKE_PASSWORD=your_password")
    print("\n5. Run this test again")
    print("="*50)


def main():
    success = test_snowflake_connection()
    
    if not success:
        print_setup_instructions()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())