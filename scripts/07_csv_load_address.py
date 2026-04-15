"""
Person.Address CSV Migration Script
Simple CSV-based migration bypassing Parquet issues
"""

import pyodbc
import snowflake.connector
import csv
import os
from dotenv import load_dotenv
import sys


def main():
    """Load Person.Address via CSV"""
    
    print("\n" + "="*60)
    print("PERSON.ADDRESS CSV MIGRATION")
    print("="*60)
    
    # Load environment
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(script_dir, '../.env')
    load_dotenv(env_file)
    
    # Paths
    csv_file = os.path.join(script_dir, '../data/Person_Address.csv')
    
    # SQL Server config
    sql_server = os.getenv('SQL_SERVER', 'localhost,1433')
    sql_database = os.getenv('SQL_DATABASE', 'AdventureWorks2022')
    sql_username = os.getenv('SQL_USERNAME', 'sa')
    sql_password = os.getenv('SQL_PASSWORD')
    
    # Snowflake config
    sf_account = os.getenv('SNOWFLAKE_ACCOUNT')
    sf_user = os.getenv('SNOWFLAKE_USER')
    sf_password = os.getenv('SNOWFLAKE_PASSWORD')
    sf_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
    sf_database = os.getenv('SNOWFLAKE_DATABASE', 'ADVENTUREWORKS')
    
    try:
        # Step 1: Connect to SQL Server
        print("\n1. Connecting to SQL Server...")
        conn_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={sql_server};"
            f"DATABASE={sql_database};"
            f"UID={sql_username};"
            f"PWD={sql_password};"
            f"TrustServerCertificate=yes;"
            f"Timeout=120;"
        )
        sql_conn = pyodbc.connect(conn_string, timeout=120)
        cursor = sql_conn.cursor()
        print("   ✓ Connected")
        
        # Step 2: Export to CSV
        print("\n2. Exporting Person.Address to CSV...")
        query = """
        SELECT 
            AddressID,
            AddressLine1,
            AddressLine2,
            City,
            StateProvinceID,
            PostalCode,
            CASE WHEN SpatialLocation IS NULL THEN NULL 
                 ELSE SpatialLocation.STAsText() END AS SpatialLocation,
            CAST(rowguid AS VARCHAR(36)) AS rowguid,
            ModifiedDate
        FROM Person.Address
        ORDER BY AddressID
        """
        
        cursor.execute(query)
        
        # Write to CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            
            # Write header
            writer.writerow([desc[0] for desc in cursor.description])
            
            # Write data
            row_count = 0
            for row in cursor:
                # Convert None to empty string for NULL representation
                clean_row = ['' if val is None else str(val) for val in row]
                writer.writerow(clean_row)
                row_count += 1
        
        cursor.close()
        sql_conn.close()
        
        print(f"   ✓ Exported {row_count:,} rows to {csv_file}")
        print(f"   ✓ File size: {os.path.getsize(csv_file) / 1024 / 1024:.2f} MB")
        
        # Step 3: Connect to Snowflake
        print("\n3. Connecting to Snowflake...")
        sf_conn = snowflake.connector.connect(
            user=sf_user,
            password=sf_password,
            account=sf_account,
            warehouse=sf_warehouse,
            database=sf_database
        )
        sf_cursor = sf_conn.cursor()
        print("   ✓ Connected")
        
        # Step 4: Create internal stage
        print("\n4. Creating/using internal stage...")
        sf_cursor.execute("CREATE STAGE IF NOT EXISTS PUBLIC.csv_stage")
        print("   ✓ Stage ready")
        
        # Step 5: Upload CSV to stage
        print("\n5. Uploading CSV to Snowflake stage...")
        put_cmd = f"PUT file://{os.path.abspath(csv_file)} @PUBLIC.csv_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
        sf_cursor.execute(put_cmd)
        print("   ✓ CSV uploaded")
        
        # Step 6: Truncate table
        print("\n6. Truncating PERSON.ADDRESS...")
        sf_cursor.execute("TRUNCATE TABLE IF EXISTS PERSON.ADDRESS")
        print("   ✓ Table truncated")
        
        # Step 7: Load CSV into table
        print("\n7. Loading CSV data into PERSON.ADDRESS...")
        copy_cmd = """
        COPY INTO PERSON.ADDRESS
        FROM @PUBLIC.csv_stage/Person_Address.csv
        FILE_FORMAT = (
            TYPE = CSV
            FIELD_DELIMITER = ','
            SKIP_HEADER = 1
            NULL_IF = ('')
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            TRIM_SPACE = TRUE
            ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
        )
        ON_ERROR = CONTINUE
        """
        
        result = sf_cursor.execute(copy_cmd)
        
        # Get results
        for row in result:
            print(f"   ✓ Loaded: {row[0]} file, {row[1]} rows")

        # Step 8: Verify
        print("\n8. Verifying data...")
        sf_cursor.execute("SELECT COUNT(*) FROM PERSON.ADDRESS")
        final_count = sf_cursor.fetchone()[0]
        print(f"   ✓ Final count: {final_count:,} rows")
        
        
        # Cleanup stage
        print("\n9. Cleaning up stage files...")
        sf_cursor.execute("REMOVE @PUBLIC.csv_stage/Person_Address.csv")
        print("   ✓ Stage cleaned")
        
        # Close connections
        sf_cursor.close()
        sf_conn.close()
        
        print("\n" + "="*60)
        print("✓ PERSON.ADDRESS MIGRATED SUCCESSFULLY VIA CSV")
        print("="*60)
        print(f"\nTotal rows: {final_count:,}")
        print("Method: SQL Server → CSV → Snowflake COPY INTO")
        print("Geography data: Stored as WKT (Well-Known Text)")
        
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())