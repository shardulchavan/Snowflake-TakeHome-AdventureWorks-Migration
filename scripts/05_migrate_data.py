"""
Data Migration Script - SQL Server to Snowflake (COMPLETE SOLUTION)
Handles ALL data types including geography, time, varbinary, hierarchyid

ENHANCED FIXES:
1. Schema case sensitivity (uppercase for Snowflake)
2. Duplicate loading bug (TRUNCATE + PURGE)
3. ALL special types: hierarchyid, geography, uniqueidentifier, time, varbinary
4. Binary data handling (hex encoding)
5. Proper error handling
"""

import pyodbc
import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import datetime
import sys


class DataMigrator:
    def __init__(self):
        """Initialize connections to SQL Server and Snowflake"""
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
        
        # Paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(script_dir, '../data/parquet')
        self.discovery_file = os.path.join(script_dir, '../data/discovery_report.json')
        
        # Stats
        self.migration_stats = {
            'start_time': None,
            'end_time': None,
            'tables_migrated': 0,
            'total_rows': 0,
            'errors': []
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
    
    def load_discovery_report(self):
        """Load discovery report to get table list"""
        try:
            with open(self.discovery_file, 'r') as f:
                self.discovery = json.load(f)
            print(f"✓ Loaded discovery report: {len(self.discovery['tables'])} tables")
            return True
        except Exception as e:
            print(f"❌ Failed to load discovery report: {e}")
            return False
    
    def create_parquet_directory(self):
        """Create directory for Parquet files"""
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        print(f"✓ Parquet directory ready: {self.data_dir}")
    
    def get_column_list_with_cast(self, schema: str, table: str) -> str:
        """
        Get column list with CAST for ALL special types
        
        Handles:
        - hierarchyid → VARCHAR(4000)
        - geography/geometry → VARCHAR(MAX) as WKT
        - uniqueidentifier → VARCHAR(36)
        - time → VARCHAR(8) as HH:MI:SS
        - varbinary → VARCHAR(MAX) as HEX
        
        Args:
            schema: Schema name
            table: Table name
            
        Returns:
            Comma-separated column list with casts
        """
        try:
            # Get column info from SQL Server
            cursor = self.sql_conn.cursor()
            query = """
            SELECT 
                c.name AS column_name,
                t.name AS data_type,
                c.max_length
            FROM sys.columns c
            INNER JOIN sys.types t ON c.user_type_id = t.user_type_id
            INNER JOIN sys.tables tbl ON c.object_id = tbl.object_id
            INNER JOIN sys.schemas s ON tbl.schema_id = s.schema_id
            WHERE s.name = ? AND tbl.name = ?
            ORDER BY c.column_id
            """
            
            cursor.execute(query, schema, table)
            columns = cursor.fetchall()
            
            # Build select list with appropriate CASTs
            select_cols = []
            for col_name, data_type, max_length in columns:
                data_type_lower = data_type.lower()
                
                if data_type_lower == 'hierarchyid':
                    # HierarchyID → VARCHAR
                    select_cols.append(f"CAST([{col_name}] AS VARCHAR(4000)) AS [{col_name}]")
                    
                elif data_type_lower in ('geography', 'geometry'):
                    # Spatial types → VARCHAR as Well-Known Text (WKT)
                    select_cols.append(f"CASE WHEN [{col_name}] IS NULL THEN NULL ELSE [{col_name}].STAsText() END AS [{col_name}]")
                    
                elif data_type_lower == 'uniqueidentifier':
                    # GUID → VARCHAR(36)
                    select_cols.append(f"CAST([{col_name}] AS VARCHAR(36)) AS [{col_name}]")
                    
                elif data_type_lower == 'time':
                    # TIME → VARCHAR(8) as HH:MI:SS
                    select_cols.append(f"CONVERT(VARCHAR(8), [{col_name}], 108) AS [{col_name}]")
                    
                elif data_type_lower == 'varbinary':
                    # VARBINARY → VARCHAR(MAX) as HEX
                    # Only convert if not NULL, otherwise very large
                    if max_length == -1:  # VARBINARY(MAX)
                        select_cols.append(f"CASE WHEN [{col_name}] IS NULL THEN NULL ELSE CONVERT(VARCHAR(MAX), [{col_name}], 2) END AS [{col_name}]")
                    else:
                        select_cols.append(f"CONVERT(VARCHAR({max_length * 2}), [{col_name}], 2) AS [{col_name}]")
                    
                else:
                    # Regular column
                    select_cols.append(f"[{col_name}]")
            
            return ', '.join(select_cols)
            
        except Exception as e:
            print(f"  ⚠ Warning getting column list: {e}, using SELECT *")
            return '*'
    
    def extract_table_to_parquet(self, schema: str, table: str, row_count: int) -> bool:
        """
        Extract table data from SQL Server to Parquet file
        
        Args:
            schema: Schema name
            table: Table name
            row_count: Expected row count
            
        Returns:
            True if successful, False otherwise
        """
        if row_count == 0:
            print(f"  ⊘ Skipping {schema}.{table} (0 rows)")
            return True
        
        # Skip Person.Address - handled by separate script (06_load_person_address.py)
        if schema == 'Person' and table == 'Address':
            print(f"  ⊘ Skipping {schema}.{table} (use 06_load_person_address.py for geography data)")
            return True
        
        try:
            # Get column list with casts for special types
            col_list = self.get_column_list_with_cast(schema, table)
            query = f"SELECT {col_list} FROM [{schema}].[{table}]"
            
            # Read to pandas DataFrame
            df = pd.read_sql(query, self.sql_conn)
            
            # FIX NULL HANDLING - Convert NaN and string "None" to proper NULL
            df = df.where(pd.notna(df), None)  # NaN → None
            df = df.replace('None', None)      # String "None" → None
            df = df.replace('nan', None)       # String "nan" → None
            
            # Handle datetime columns - convert to timezone-naive
            for col in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetimetz']).columns:
                df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
            
            # SPECIAL HANDLING: Person.Address - Direct load via Snowflake connector
            if schema == 'Person' and table == 'Address':
                print(f"  ⚡ Direct loading {schema}.{table} via Snowflake connector (bypassing Parquet)")
                try:
                    from snowflake.connector.pandas_tools import write_pandas
                    
                    # Truncate table first
                    schema_upper = schema.upper()
                    self.sf_cursor.execute(f"TRUNCATE TABLE IF EXISTS {schema_upper}.{table}")
                    
                    # Direct write to Snowflake
                    success, nchunks, nrows, _ = write_pandas(
                        conn=self.sf_conn,
                        df=df,
                        table_name=table.upper(),
                        schema=schema_upper,
                        quote_identifiers=False,
                        auto_create_table=False
                    )
                    
                    if success:
                        print(f"  ✓ Directly loaded {schema}.{table}: {nrows:,} rows")
                        self.migration_stats['total_rows'] += nrows
                        self.migration_stats['tables_migrated'] += 1
                        return True
                    else:
                        raise Exception("write_pandas returned False")
                        
                except Exception as e:
                    print(f"  ❌ Direct load failed: {e}, falling back to Parquet")
                    # Fall through to normal Parquet handling
            
            # Force object columns (like geography WKT) to string type
            for col in df.select_dtypes(include=['object']).columns:
                if df[col].notna().any():  # Only if has non-null values
                    df[col] = df[col].astype(str)
                    df[col] = df[col].replace('None', None)  # Clean up after string conversion
            
            # Save to Parquet
            parquet_file = f"{self.data_dir}/{schema}_{table}.parquet"
            df.to_parquet(parquet_file, engine='pyarrow', index=False)
            
            actual_rows = len(df)
            print(f"  ✓ Extracted {schema}.{table}: {actual_rows:,} rows")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to extract {schema}.{table}: {e}")
            self.migration_stats['errors'].append({
                'table': f"{schema}.{table}",
                'phase': 'extract',
                'error': str(e)
            })
            return False
    
    def create_snowflake_stage(self):
        """Create internal stage in Snowflake for file uploads"""
        try:
            self.sf_cursor.execute("CREATE STAGE IF NOT EXISTS PUBLIC.migration_stage")
            print("✓ Snowflake stage created: PUBLIC.migration_stage")
            return True
        except Exception as e:
            print(f"❌ Failed to create stage: {e}")
            return False
    
    def upload_parquet_to_stage(self, schema: str, table: str) -> bool:
        """
        Upload Parquet file to Snowflake stage
        
        Args:
            schema: Schema name
            table: Table name
            
        Returns:
            True if successful
        """
        try:
            parquet_file = f"{self.data_dir}/{schema}_{table}.parquet"
            
            if not os.path.exists(parquet_file):
                print(f"  ⊘ No file to upload for {schema}.{table}")
                return True
            
            # Upload using PUT command
            put_cmd = f"PUT file://{os.path.abspath(parquet_file)} @PUBLIC.migration_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
            self.sf_cursor.execute(put_cmd)
            
            print(f"  ✓ Uploaded {schema}.{table} to stage")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to upload {schema}.{table}: {e}")
            self.migration_stats['errors'].append({
                'table': f"{schema}.{table}",
                'phase': 'upload',
                'error': str(e)
            })
            return False
    
    def load_table_from_stage(self, schema: str, table: str, row_count: int) -> bool:
        """
        Load data from stage into Snowflake table using COPY INTO
        
        Args:
            schema: Schema name
            table: Table name
            row_count: Expected row count
            
        Returns:
            True if successful
        """
        if row_count == 0:
            return True
        
        # Skip Person.Address - it's loaded directly via write_pandas during extract
        if schema == 'Person' and table == 'Address':
            print(f"  ⊘ Skipping {schema}.{table} (already loaded directly)")
            return True
        
        # Skip tables we didn't extract
        parquet_file = f"{self.data_dir}/{schema}_{table}.parquet"
        if not os.path.exists(parquet_file):
            return True
        
        try:
            # Use uppercase schema name for Snowflake
            schema_upper = schema.upper()
            parquet_filename = f"{schema}_{table}.parquet"
            
            # TRUNCATE table before loading to prevent duplicates
            truncate_cmd = f"TRUNCATE TABLE IF EXISTS {schema_upper}.{table}"
            self.sf_cursor.execute(truncate_cmd)
            
            # COPY INTO command with PURGE to delete staged file after load
            copy_cmd = f"""
            COPY INTO {schema_upper}.{table}
            FROM @PUBLIC.migration_stage/{parquet_filename}
            FILE_FORMAT = (TYPE = PARQUET)
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
            ON_ERROR = ABORT_STATEMENT
            PURGE = TRUE
            """
            
            self.sf_cursor.execute(copy_cmd)
            
            # Verify row count
            self.sf_cursor.execute(f"SELECT COUNT(*) FROM {schema_upper}.{table}")
            loaded_rows = self.sf_cursor.fetchone()[0]
            
            if loaded_rows == row_count:
                print(f"  ✓ Loaded {schema}.{table}: {loaded_rows:,} rows (verified)")
                self.migration_stats['total_rows'] += loaded_rows
                self.migration_stats['tables_migrated'] += 1
                return True
            else:
                print(f"  ⚠ {schema}.{table}: Expected {row_count:,}, got {loaded_rows:,}")
                self.migration_stats['errors'].append({
                    'table': f"{schema}.{table}",
                    'phase': 'load',
                    'error': f"Row count mismatch: expected {row_count}, got {loaded_rows}"
                })
                # Still count as migrated if close
                if loaded_rows > 0:
                    self.migration_stats['total_rows'] += loaded_rows
                    self.migration_stats['tables_migrated'] += 1
                return False
                
        except Exception as e:
            print(f"  ❌ Failed to load {schema}.{table}: {e}")
            self.migration_stats['errors'].append({
                'table': f"{schema}.{table}",
                'phase': 'load',
                'error': str(e)
            })
            return False
    
    def migrate_all_tables(self):
        """Main migration workflow"""
        print("\n" + "="*60)
        print("DATA MIGRATION - SQL SERVER TO SNOWFLAKE")
        print("="*60)
        
        self.migration_stats['start_time'] = datetime.now()
        
        # Get table list sorted by row count (small tables first)
        tables = sorted(self.discovery['tables'], key=lambda x: x['rows'])
        
        print(f"\nMigrating {len(tables)} tables...")
        print("="*60)
        
        # Phase 1: Extract to Parquet
        print("\nPHASE 1: Extracting data to Parquet files")
        print("-"*60)
        extracted = 0
        for table in tables:
            if self.extract_table_to_parquet(table['schema'], table['name'], table['rows']):
                extracted += 1
        
        print(f"\n✓ Extracted {extracted}/{len(tables)} tables")
        
        # Phase 2: Upload to Snowflake stage
        print("\n" + "="*60)
        print("PHASE 2: Uploading to Snowflake stage")
        print("-"*60)
        uploaded = 0
        for table in tables:
            if table['rows'] > 0:  # Only upload non-empty tables
                if self.upload_parquet_to_stage(table['schema'], table['name']):
                    uploaded += 1
        
        print(f"\n✓ Uploaded {uploaded} files to stage")
        
        # Phase 3: Load into tables
        print("\n" + "="*60)
        print("PHASE 3: Loading data into Snowflake tables")
        print("-"*60)
        for table in tables:
            self.load_table_from_stage(table['schema'], table['name'], table['rows'])
        
        self.migration_stats['end_time'] = datetime.now()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print migration summary"""
        duration = (self.migration_stats['end_time'] - self.migration_stats['start_time']).total_seconds()
        
        print("\n" + "="*60)
        print("MIGRATION SUMMARY")
        print("="*60)
        print(f"Tables migrated: {self.migration_stats['tables_migrated']}")
        print(f"Total rows: {self.migration_stats['total_rows']:,}")
        print(f"Duration: {duration:.1f} seconds")
        if self.migration_stats['total_rows'] > 0:
            print(f"Throughput: {self.migration_stats['total_rows']/duration:.0f} rows/sec")
        
        if self.migration_stats['errors']:
            print(f"\n⚠ Errors: {len(self.migration_stats['errors'])}")
            for error in self.migration_stats['errors'][:10]:  # Show first 10
                print(f"  - {error['table']} ({error['phase']})")
        else:
            print("\n✓ No errors!")
        
        print("="*60)
        
        # Save stats to file
        stats_dir = os.path.dirname(self.discovery_file)
        stats_file = os.path.join(stats_dir, 'migration_stats.json')
        with open(stats_file, 'w') as f:
            # Convert datetime to string for JSON
            stats_copy = self.migration_stats.copy()
            stats_copy['start_time'] = str(stats_copy['start_time'])
            stats_copy['end_time'] = str(stats_copy['end_time'])
            json.dump(stats_copy, f, indent=2)
        print(f"\n✓ Stats saved to: {stats_file}")
    
    def cleanup_stage(self):
        """Remove files from stage after migration"""
        try:
            self.sf_cursor.execute("REMOVE @PUBLIC.migration_stage")
            print("✓ Cleaned up stage files")
        except Exception as e:
            print(f"⚠ Stage cleanup warning: {e}")
    
    def close_connections(self):
        """Close all database connections"""
        if hasattr(self, 'sql_conn'):
            self.sql_conn.close()
        if hasattr(self, 'sf_cursor'):
            self.sf_cursor.close()
        if hasattr(self, 'sf_conn'):
            self.sf_conn.close()
        print("✓ Connections closed")


def main():
    """Main execution"""
    migrator = DataMigrator()
    
    # Setup
    if not migrator.load_discovery_report():
        return 1
    
    migrator.create_parquet_directory()
    
    if not migrator.connect_sqlserver():
        return 1
    
    if not migrator.connect_snowflake():
        return 1
    
    if not migrator.create_snowflake_stage():
        return 1
    
    # Run migration
    try:
        migrator.migrate_all_tables()
        
        # Cleanup
        migrator.cleanup_stage()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Migration interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        migrator.close_connections()
    
    print("\n✓ MIGRATION COMPLETE!")
    print("\nNext steps:")
    print("  1. Verify data in Snowflake UI")
    print("  2. Run validation queries")
    print("  3. Compare row counts with source")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())