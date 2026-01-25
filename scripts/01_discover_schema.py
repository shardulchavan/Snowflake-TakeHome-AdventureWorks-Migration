"""
AdventureWorks Schema Discovery Script
Extracts complete metadata from SQL Server for migration planning
"""

import pyodbc
import json
from datetime import datetime
from typing import Dict, List
import sys

class SchemaDiscovery:
    def __init__(self, server: str, database: str, username: str, password: str):
        """Initialize connection to SQL Server"""
        self.conn_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
        self.database = database
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = pyodbc.connect(self.conn_string)
            self.cursor = self.conn.cursor()
            print(f"✓ Connected to {self.database}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def get_tables(self) -> List[Dict]:
        """Extract all user tables with row counts"""
        query = """
        SELECT 
            s.name AS schema_name,
            t.name AS table_name,
            p.rows AS row_count
        FROM sys.tables t
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        INNER JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0,1)
        AND s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, t.name
        """
        
        self.cursor.execute(query)
        tables = []
        for row in self.cursor.fetchall():
            tables.append({
                'schema': row.schema_name,
                'name': row.table_name,
                'rows': row.row_count
            })
        
        print(f"✓ Found {len(tables)} tables")
        return tables
    
    def get_columns(self, schema: str, table: str) -> List[Dict]:
        """Extract column metadata for a specific table"""
        query = """
        SELECT 
            c.name AS column_name,
            t.name AS data_type,
            c.max_length,
            c.precision,
            c.scale,
            c.is_nullable,
            c.is_identity
        FROM sys.columns c
        INNER JOIN sys.types t ON c.user_type_id = t.user_type_id
        INNER JOIN sys.tables tbl ON c.object_id = tbl.object_id
        INNER JOIN sys.schemas s ON tbl.schema_id = s.schema_id
        WHERE s.name = ? AND tbl.name = ?
        ORDER BY c.column_id
        """
        
        self.cursor.execute(query, schema, table)
        columns = []
        for row in self.cursor.fetchall():
            columns.append({
                'name': row.column_name,
                'data_type': row.data_type,
                'max_length': row.max_length,
                'precision': row.precision,
                'scale': row.scale,
                'nullable': row.is_nullable,
                'is_identity': row.is_identity
            })
        
        return columns
    
    def get_primary_keys(self) -> List[Dict]:
        """Extract primary key constraints"""
        query = """
        SELECT 
            s.name AS schema_name,
            t.name AS table_name,
            i.name AS pk_name,
            STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS columns
        FROM sys.indexes i
        INNER JOIN sys.tables t ON i.object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
        INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        WHERE i.is_primary_key = 1
        GROUP BY s.name, t.name, i.name
        ORDER BY s.name, t.name
        """
        
        self.cursor.execute(query)
        pks = []
        for row in self.cursor.fetchall():
            pks.append({
                'schema': row.schema_name,
                'table': row.table_name,
                'name': row.pk_name,
                'columns': row.columns
            })
        
        print(f"✓ Found {len(pks)} primary keys")
        return pks
    
    def get_foreign_keys(self) -> List[Dict]:
        """Extract foreign key constraints"""
        query = """
        SELECT 
            s.name AS schema_name,
            t.name AS table_name,
            fk.name AS fk_name,
            rs.name AS ref_schema,
            rt.name AS ref_table,
            STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY fkc.constraint_column_id) AS columns,
            STRING_AGG(rc.name, ', ') WITHIN GROUP (ORDER BY fkc.constraint_column_id) AS ref_columns
        FROM sys.foreign_keys fk
        INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        INNER JOIN sys.tables rt ON fk.referenced_object_id = rt.object_id
        INNER JOIN sys.schemas rs ON rt.schema_id = rs.schema_id
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.columns c ON fkc.parent_object_id = c.object_id AND fkc.parent_column_id = c.column_id
        INNER JOIN sys.columns rc ON fkc.referenced_object_id = rc.object_id AND fkc.referenced_column_id = rc.column_id
        GROUP BY s.name, t.name, fk.name, rs.name, rt.name
        ORDER BY s.name, t.name
        """
        
        self.cursor.execute(query)
        fks = []
        for row in self.cursor.fetchall():
            fks.append({
                'schema': row.schema_name,
                'table': row.table_name,
                'name': row.fk_name,
                'ref_schema': row.ref_schema,
                'ref_table': row.ref_table,
                'columns': row.columns,
                'ref_columns': row.ref_columns
            })
        
        print(f"✓ Found {len(fks)} foreign keys")
        return fks
    
    def get_views(self) -> List[Dict]:
        """Extract view definitions"""
        query = """
        SELECT 
            s.name AS schema_name,
            v.name AS view_name
        FROM sys.views v
        INNER JOIN sys.schemas s ON v.schema_id = s.schema_id
        WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, v.name
        """
        
        self.cursor.execute(query)
        views = []
        for row in self.cursor.fetchall():
            views.append({
                'schema': row.schema_name,
                'name': row.view_name
            })
        
        print(f"✓ Found {len(views)} views")
        return views
    
    def get_stored_procedures(self) -> List[Dict]:
        """Extract stored procedure names"""
        query = """
        SELECT 
            s.name AS schema_name,
            p.name AS proc_name
        FROM sys.procedures p
        INNER JOIN sys.schemas s ON p.schema_id = s.schema_id
        WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, p.name
        """
        
        self.cursor.execute(query)
        procs = []
        for row in self.cursor.fetchall():
            procs.append({
                'schema': row.schema_name,
                'name': row.proc_name
            })
        
        print(f"✓ Found {len(procs)} stored procedures")
        return procs
    
    def run_discovery(self) -> Dict:
        """Execute complete discovery process"""
        print("\n=== Starting Schema Discovery ===\n")
        
        if not self.connect():
            return None
        
        # Get all tables first
        tables = self.get_tables()
        
        # Enrich tables with column information
        print("\nExtracting column metadata...")
        for table in tables:
            table['columns'] = self.get_columns(table['schema'], table['name'])
        print(f"✓ Column metadata complete")
        
        # Get constraints
        primary_keys = self.get_primary_keys()
        foreign_keys = self.get_foreign_keys()
        
        # Get code objects
        views = self.get_views()
        procedures = self.get_stored_procedures()
        
        # Compile report
        discovery_data = {
            'metadata': {
                'database': self.database,
                'discovery_date': datetime.now().isoformat(),
                'total_tables': len(tables),
                'total_rows': sum(t['rows'] for t in tables),
                'total_views': len(views),
                'total_procedures': len(procedures)
            },
            'tables': tables,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys,
            'views': views,
            'stored_procedures': procedures
        }
        
        self.conn.close()
        print("\n✓ Discovery complete")
        return discovery_data
    
    def save_report(self, data: Dict, filename: str):
        """Save discovery data to JSON file"""
        import os
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"\n✓ Report saved to: {filename}")


def main():
    # Configuration
    config = {
        'server': 'localhost,1433',
        'database': 'AdventureWorks2022',
        'username': 'sa',
        'password': 'YourStrong@Passw0rd'
    }
    
    # Run discovery
    discovery = SchemaDiscovery(**config)
    data = discovery.run_discovery()
    
    if data:
        # Save full report
        discovery.save_report(data, '../data/discovery_report.json')
        
        # Print summary
        print("\n" + "="*50)
        print("DISCOVERY SUMMARY")
        print("="*50)
        print(f"Database: {data['metadata']['database']}")
        print(f"Tables: {data['metadata']['total_tables']}")
        print(f"Total Rows: {data['metadata']['total_rows']:,}")
        print(f"Views: {data['metadata']['total_views']}")
        print(f"Stored Procedures: {data['metadata']['total_procedures']}")
        print(f"Primary Keys: {len(data['primary_keys'])}")
        print(f"Foreign Keys: {len(data['foreign_keys'])}")
        print("="*50)
        
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())