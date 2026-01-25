"""
Schema Conversion Script - SQL Server to Snowflake
Converts discovery report into Snowflake-compatible DDL statements
"""

import json
import os
from typing import Dict, List, Tuple
from pathlib import Path


class SchemaConverter:
    def __init__(self, discovery_file: str, mapping_file: str):
        """Initialize converter with discovery data and type mappings"""
        
        # Load discovery report
        with open(discovery_file, 'r') as f:
            self.discovery = json.load(f)
        
        # Load type mappings
        with open(mapping_file, 'r') as f:
            self.type_mapping = json.load(f)
        
        self.conversion_log = []
    
    def normalize_schema_name(self, schema: str) -> str:
        """Convert schema name to TitleCase (DBO stays as DBO)"""
        if schema.lower() == 'dbo':
            return 'DBO'
        return schema.title()
        
    def log_conversion(self, category: str, message: str):
        """Log conversion decisions"""
        self.conversion_log.append({
            'category': category,
            'message': message
        })
        print(f"[{category}] {message}")
    
    def map_data_type(self, sql_type: str, max_length: int, precision: int, scale: int) -> str:
        """
        Convert SQL Server data type to Snowflake equivalent
        
        Args:
            sql_type: SQL Server data type name
            max_length: Maximum length for string/binary types
            precision: Numeric precision
            scale: Numeric scale
            
        Returns:
            Snowflake data type definition
        """
        sql_type_lower = sql_type.lower()
        
        # Check if type exists in mapping
        if sql_type_lower not in self.type_mapping['mappings']:
            self.log_conversion('WARNING', f"Unmapped type: {sql_type}, defaulting to VARCHAR")
            return "VARCHAR(16777216)"
        
        mapping = self.type_mapping['mappings'][sql_type_lower]
        snowflake_type = mapping['snowflake_type']
        
        # Handle types that use source precision/scale
        if mapping.get('use_source_precision'):
            if precision > 0:
                return f"{snowflake_type}({precision},{scale})"
            else:
                return f"{snowflake_type}(38,0)"
        
        # Handle string types with length
        if mapping.get('use_source_length'):
            # Special case: VARCHAR(MAX) or NVARCHAR(MAX)
            if max_length == -1:
                length = self.type_mapping['special_cases']['varchar_max']['snowflake_length']
            else:
                length = max_length
                # Adjust for NVARCHAR (2 bytes per char in SQL Server)
                if sql_type_lower.startswith('n') and length > 0:
                    if self.type_mapping['special_cases']['nvarchar_max_length_adjustment']['apply']:
                        length = length // 2
            
            return f"{snowflake_type}({length})" if length > 0 else snowflake_type
        
        # Handle types with predefined precision
        if 'precision' in mapping:
            if 'scale' in mapping:
                return f"{snowflake_type}({mapping['precision']},{mapping['scale']})"
            else:
                return f"{snowflake_type}({mapping['precision']})"
        
        return snowflake_type
    
    def generate_schemas_sql(self) -> str:
        """Generate CREATE SCHEMA statements"""
        schemas = set()
        for table in self.discovery['tables']:
            schemas.add(table['schema'])
        
        sql = ["-- ============================================="]
        sql.append("-- Schema Creation")
        sql.append("-- =============================================")
        sql.append("")
        
        for schema in sorted(schemas):
            # Convert to TitleCase
            schema_titlecase = self.normalize_schema_name(schema)
            sql.append(f"CREATE SCHEMA IF NOT EXISTS {schema_titlecase};")
            self.log_conversion('SCHEMA', f"Created schema: {schema_titlecase}")
        
        return "\n".join(sql)
    
    def generate_sequence_for_identity(self, schema: str, table: str, column: str) -> str:
        """Generate sequence for identity column"""
        seq_name = f"{schema}_{table}_{column}_seq".upper()
        sql = f"CREATE SEQUENCE IF NOT EXISTS {schema}.{seq_name} START = 1 INCREMENT = 1;"
        return sql
    
    def generate_tables_sql(self) -> Tuple[str, List[str]]:
        """
        Generate CREATE TABLE statements
        Returns tuple of (sql_string, list_of_sequences)
        """
        sql = ["-- ============================================="]
        sql.append("-- Table Creation")
        sql.append("-- =============================================")
        sql.append("")
        
        sequences = []
        
        for table in self.discovery['tables']:
            schema = table['schema']
            schema = self.normalize_schema_name(schema)  # Convert to TitleCase
            table_name = table['name']
            
            sql.append(f"-- Table: {schema}.{table_name} ({table['rows']:,} rows)")
            sql.append(f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} (")
            
            columns = []
            for col in table['columns']:
                col_name = col['name']
                
                # Map data type
                sf_type = self.map_data_type(
                    col['data_type'],
                    col['max_length'],
                    col['precision'],
                    col['scale']
                )
                
                # Handle NULL/NOT NULL
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                
                # Quote column name if has spaces or is reserved keyword
                reserved_keywords = {'group', 'user', 'order', 'select', 'from', 'where', 'table', 'schema'}
                col_name_quoted = f'"{col_name}"' if ' ' in col_name or col_name.lower() in reserved_keywords else col_name

                # Handle identity columns
                if col['is_identity']:
                    seq_name = f"{schema}_{table_name}_{col_name}_seq".upper()
                    default_clause = f"DEFAULT {schema}.{seq_name}.NEXTVAL"
                    sequences.append(self.generate_sequence_for_identity(schema, table_name, col_name))
                    col_def = f"    {col_name_quoted} {sf_type} {default_clause} {nullable}"
                    self.log_conversion('IDENTITY', f"Converted identity: {schema}.{table_name}.{col_name}")
                else:
                    col_def = f"    {col_name_quoted} {sf_type} {nullable}"
                
                columns.append(col_def)
            
            sql.append(",\n".join(columns))
            sql.append(");")
            sql.append("")
            
            self.log_conversion('TABLE', f"Converted table: {schema}.{table_name}")
        
        return "\n".join(sql), sequences
    
    def generate_primary_keys_sql(self) -> str:
        """Generate PRIMARY KEY constraints (informational in Snowflake)"""
        sql = ["-- ============================================="]
        sql.append("-- Primary Key Constraints (Informational)")
        sql.append("-- Note: Snowflake doesn't enforce PKs, but they aid query optimization")
        sql.append("-- =============================================")
        sql.append("")
        
        for pk in self.discovery['primary_keys']:
            schema = self.normalize_schema_name(pk['schema'])
            table = pk['table']
            pk_name = pk['name']
            columns = pk['columns']
            
            # Snowflake syntax for informational PK
            sql.append(f"ALTER TABLE {schema}.{table}")
            sql.append(f"    ADD CONSTRAINT {pk_name} PRIMARY KEY ({columns}) NOT ENFORCED;")
            sql.append("")
            
            self.log_conversion('PK', f"Created PK: {schema}.{table}")
        
        return "\n".join(sql)
    
    def generate_foreign_keys_sql(self) -> str:
        """Generate FOREIGN KEY constraints (informational in Snowflake)"""
        sql = ["-- ============================================="]
        sql.append("-- Foreign Key Constraints (Informational)")
        sql.append("-- Note: Snowflake doesn't enforce FKs, but they aid query optimization")
        sql.append("-- =============================================")
        sql.append("")
        
        for fk in self.discovery['foreign_keys']:
            schema = self.normalize_schema_name(fk['schema'])
            table = fk['table']
            fk_name = fk['name']
            columns = fk['columns']
            ref_schema = self.normalize_schema_name(fk['ref_schema'])
            ref_table = fk['ref_table']
            ref_columns = fk['ref_columns']
            
            sql.append(f"ALTER TABLE {schema}.{table}")
            sql.append(f"    ADD CONSTRAINT {fk_name}")
            sql.append(f"    FOREIGN KEY ({columns})")
            sql.append(f"    REFERENCES {ref_schema}.{ref_table}({ref_columns})")
            sql.append(f"    NOT ENFORCED;")
            sql.append("")
            
            self.log_conversion('FK', f"Created FK: {schema}.{table} -> {ref_schema}.{ref_table}")
        
        return "\n".join(sql)
    
    def generate_sequences_sql(self, sequences: List[str]) -> str:
        """Generate all sequence creation statements"""
        if not sequences:
            return ""
        
        sql = ["-- ============================================="]
        sql.append("-- Sequences (for Identity Columns)")
        sql.append("-- =============================================")
        sql.append("")
        sql.extend(sequences)
        
        return "\n".join(sql)
    
    def save_conversion_report(self, output_dir: str):
        """Save conversion log and statistics"""
        report = {
            'source_database': self.discovery['metadata']['database'],
            'conversion_date': self.discovery['metadata']['discovery_date'],
            'statistics': {
                'schemas': len(set(t['schema'] for t in self.discovery['tables'])),
                'tables': len(self.discovery['tables']),
                'primary_keys': len(self.discovery['primary_keys']),
                'foreign_keys': len(self.discovery['foreign_keys'])
            },
            'conversion_log': self.conversion_log
        }
        
        report_file = os.path.join(output_dir, 'conversion_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Conversion report saved: {report_file}")
    
    def run_conversion(self, output_dir: str):
        """Execute complete conversion process"""
        print("\n=== Starting Schema Conversion ===\n")
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate schemas
        print("\nGenerating schemas...")
        schemas_sql = self.generate_schemas_sql()
        with open(os.path.join(output_dir, '01_schemas.sql'), 'w') as f:
            f.write(schemas_sql)
        
        # Generate sequences and tables
        print("\nGenerating tables and sequences...")
        tables_sql, sequences = self.generate_tables_sql()
        sequences_sql = self.generate_sequences_sql(sequences)
        
        with open(os.path.join(output_dir, '02_sequences.sql'), 'w') as f:
            f.write(sequences_sql)
        
        with open(os.path.join(output_dir, '03_tables.sql'), 'w') as f:
            f.write(tables_sql)
        
        # Generate constraints
        print("\nGenerating constraints...")
        pk_sql = self.generate_primary_keys_sql()
        with open(os.path.join(output_dir, '04_primary_keys.sql'), 'w') as f:
            f.write(pk_sql)
        
        fk_sql = self.generate_foreign_keys_sql()
        with open(os.path.join(output_dir, '05_foreign_keys.sql'), 'w') as f:
            f.write(fk_sql)
        
        # Save conversion report
        self.save_conversion_report(output_dir)
        
        print("\n" + "="*50)
        print("CONVERSION COMPLETE")
        print("="*50)
        print(f"Output directory: {output_dir}")
        print(f"Files generated:")
        print(f"  - 01_schemas.sql")
        print(f"  - 02_sequences.sql")
        print(f"  - 03_tables.sql")
        print(f"  - 04_primary_keys.sql")
        print(f"  - 05_foreign_keys.sql")
        print(f"  - conversion_report.json")
        print("="*50)


def main():
    # File paths - use absolute paths or handle relative correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    discovery_file = os.path.join(script_dir, '../data/discovery_report.json')
    mapping_file = os.path.join(script_dir, '../config/type_mapping.json')
    output_dir = os.path.join(script_dir, '../snowflake_ddl')
    
    # Check if discovery report exists
    if not os.path.exists(discovery_file):
        print(f"ERROR: Discovery report not found: {discovery_file}")
        print("Please run 01_discover_schema.py first")
        return 1
    
    # Run conversion
    converter = SchemaConverter(discovery_file, mapping_file)
    converter.run_conversion(output_dir)
    
    return 0


if __name__ == "__main__":
    exit(main())