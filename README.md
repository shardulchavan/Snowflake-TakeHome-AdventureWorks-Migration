# AdventureWorks: SQL Server to Snowflake Migration

A complete, automated migration framework that moves Microsoft's AdventureWorks database from SQL Server to Snowflake. Built to demonstrate production-ready database migration practices with real-world complexity handling.

---

## 🎯 What This Project Does

This isn't just a simple data copy—it's a **comprehensive migration pipeline** that:

1. **Discovers** your SQL Server schema automatically (no manual documentation needed)
2. **Converts** SQL Server DDL to Snowflake-compatible SQL (handles 30+ data type mappings)
3. **Migrates** 760,000+ rows efficiently using Apache Parquet (columnar format = fast!)
4. **Validates** everything worked (automated row count checks, integrity verification)
5. **Handles edge cases** like spatial data, binary blobs, and SQL Server-specific types

**Real-world challenge:** Not all data types translate cleanly. This project shows how to handle hierarchyid, geography, time, and varbinary types that typically break automated migrations.

---

## 📊 Migration Results

**Final Stats:**
- ✅ **71/71 tables** migrated (100% coverage)
- ✅ **760,837 rows** across 6 business schemas
- ✅ **~3 minutes** total migration time
- ✅ **Zero manual intervention** required

**Schema Breakdown:**
- Sales: 19 tables, 253K rows
- Production: 25 tables, 350K rows  
- Person: 13 tables, 141K rows
- HumanResources: 6 tables, 934 rows
- Purchasing: 5 tables, 13K rows
- DBO: 3 tables, 1.6K rows

---

## 🏗️ How It Works (Architecture)

```
┌─────────────────┐
│  SQL Server     │  1. Discovery: Query system catalogs
│  (Docker)       │     Extract all metadata automatically
└────────┬────────┘
         │
         ├─ 01_discover_schema.py
         │  • Queries sys.tables, sys.columns
         │  • Generates discovery_report.json
         │
         ├─ 02_convert_schema.py
         │  • Reads discovery report
         │  • Maps types: INT→NUMBER, DATETIME→TIMESTAMP_NTZ
         │  • Generates 5 SQL files (schemas, tables, constraints)
         │
┌────────▼────────┐
│  Parquet Files  │  2. Extract: SQL Server → Parquet
│  (Local Disk)   │     Columnar format = fast + compressed
└────────┬────────┘
         │
         ├─ 05_migrate_data.py
         │  • Reads tables with pandas
         │  • Casts special types (hierarchyid→VARCHAR)
         │  • Saves as .parquet files
         │
┌────────▼────────┐
│ Snowflake Stage │  3. Upload: PUT command → Internal stage
│ (Internal)      │     Snowflake's S3-backed temp storage
└────────┬────────┘
         │
         ├─ COPY INTO commands
         │  • Parallel bulk loading
         │  • Automatic type inference
         │  • PURGE staged files after load
         │
┌────────▼────────┐
│   Snowflake     │  4. Validate: COUNT(*) matching
│   Tables        │     Verify row counts = success!
└─────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Why We Use It |
|-----------|-----------|---------------|
| **Infrastructure** | Docker (SQL Server 2022), Snowflake Cloud (AWS) | Reproducible environment, cloud scalability |
| **ETL Pipeline** | Python 3.10 + PyODBC + Apache Parquet + Snowflake Connector | Industry standard, efficient columnar format |
| **Staging** | Snowflake Internal Stages (PUT/COPY INTO) | Built-in parallel loading, no external S3 needed |
| **Automation** | JSON-driven type mapper, DDL generator, validation scripts | Repeatable, no manual steps |
| **Special Handling** | WKT for geography, hex for binary, CAST for hierarchyid | Handles SQL Server exotic types |

---

## 🚀 Quick Start (15 Minutes)

### Prerequisites

Install these first:
- **Docker Desktop** - Runs SQL Server without installing it
- **Python 3.9+** - For ETL scripts  
- **ODBC Driver 18** - Connects Python to SQL Server

[Detailed installation steps in docs/SETUP_GUIDE.md]

---

### Step-by-Step

```bash
# 1. Set up SQL Server (30 seconds)
docker-compose up -d                    # Starts SQL Server container
./setup/install_adventureworks.sh       # Downloads & restores database

# 2. Create Python environment (1 minute)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Discover the schema (10 seconds)
cd scripts
python 01_discover_schema.py
# → Creates data/discovery_report.json with all table metadata

# 4. Convert to Snowflake DDL (5 seconds)  
python 02_convert_schema.py
# → Generates snowflake_ddl/*.sql files

# 5. Set up Snowflake (one-time, 2 minutes)
# - Sign up at signup.snowflake.com (free trial)
# - Update .env with your credentials
python 03_test_snowflake_connection.py  # Verify it works

# 6. Create Snowflake schema (30 seconds)
python 04_execute_ddl_snowflake.py
# → Creates 6 schemas, 71 tables, 39 sequences, constraints

# 7. Migrate the data! (2-3 minutes)
python 05_migrate_data.py               # Migrates 70 tables via Parquet
python 06_load_person_address_csv.py    # Handles spatial data separately

# 8. Verify (10 seconds)
# Check in Snowflake UI: SELECT COUNT(*) FROM SALES.CUSTOMER;
```

**Done! 71 tables, 760K rows migrated.** ✅

---

## 📁 Project Structure (What Each File Does)

```
adventureworks-migration/
│
├── docker-compose.yml              # SQL Server container config
├── requirements.txt                # Python dependencies (pyodbc, snowflake-connector)
├── .env                           # Your credentials (SQL Server + Snowflake)
│
├── setup/
│   └── install_adventureworks.sh  # Downloads AdventureWorks backup, restores to SQL Server
│
├── config/
│   └── type_mapping.json          # SQL Server→Snowflake type conversion rules
│                                   # (INT→NUMBER, DATETIME→TIMESTAMP_NTZ, etc.)
│
├── scripts/
│   ├── 01_discover_schema.py      # Queries SQL Server metadata, saves JSON
│   ├── 02_convert_schema.py       # Reads JSON, generates Snowflake DDL
│   ├── 03_test_snowflake.py       # Connection test (before migration)
│   ├── 04_execute_ddl.py          # Runs DDL in Snowflake (creates tables)
│   ├── 05_migrate_data.py         # Extract→Parquet→Snowflake (70 tables)
│   └── 06_load_person_address_csv.py  # Special CSV handler for spatial data
│
├── snowflake_ddl/                 # Generated SQL files
│   ├── 01_schemas.sql             # CREATE SCHEMA statements
│   ├── 02_sequences.sql           # Sequences for identity columns
│   ├── 03_tables.sql              # CREATE TABLE (all 71 tables)
│   ├── 04_primary_keys.sql        # Primary key constraints
│   └── 05_foreign_keys.sql        # Foreign key constraints
│
└── data/
    ├── discovery_report.json      # Schema metadata from SQL Server
    ├── parquet/                   # Extracted data files (temporary)
    └── migration_stats.json       # Final statistics
```

---

## 🔧 Key Scripts Explained

### **01_discover_schema.py** - The Detective
**What it does:** Connects to SQL Server and asks "What tables exist? What columns? What types?"

**How it works:**
```python
# Queries SQL Server system tables
SELECT t.name, c.name, c.data_type, c.max_length
FROM sys.tables t JOIN sys.columns c ON t.object_id = c.object_id

# Saves everything to JSON for next scripts
```

**Output:** Complete inventory of 71 tables with all metadata

---

### **02_convert_schema.py** - The Translator
**What it does:** Converts SQL Server DDL → Snowflake DDL

**How it works:**
```python
# Reads type_mapping.json rules:
INT → NUMBER(38,0)
DATETIME → TIMESTAMP_NTZ  
NVARCHAR(50) → VARCHAR(25)  # Adjusts for Unicode

# Special handling:
Identity columns → Sequences
Clustered indexes → Clustering keys
```

**Output:** 5 .sql files ready to run in Snowflake

---

### **05_migrate_data.py** - The Mover
**What it does:** Bulk data transfer using Parquet (fast columnar format)

**How it works:**
```python
# For each table:
1. Extract: SELECT * FROM SQL_Server → pandas DataFrame
2. Transform: Handle special types (hierarchyid→VARCHAR, time→HH:MI:SS)
3. Save: DataFrame → Parquet file (compressed, typed)
4. Upload: PUT file to Snowflake internal stage
5. Load: COPY INTO table FROM stage (parallel bulk insert)
6. Verify: COUNT(*) matches source
```

**Why Parquet?** 3-5x faster than CSV, preserves data types, compressed

---

### **06_load_person_address_csv.py** - The Specialist
**What it does:** Handles Person.Address table with geography data

**Why separate?** SQL Server geography type → WKT (Well-Known Text) string causes type inference issues in Parquet. CSV is simpler for this edge case.

**How it works:**
```python
# Extract geography as text:
SELECT SpatialLocation.STAsText() FROM Person.Address
# → "POINT (-122.164 47.786)"

# Load via CSV (no type inference issues)
COPY INTO PERSON.ADDRESS FROM @stage/address.csv
```

---

## 💡 Technical Highlights

### **Problem 1: SQL Server Identity Columns**
SQL Server has `IDENTITY(1,1)` for auto-increment. Snowflake doesn't.

**Solution:** Convert to sequences
```sql
CREATE SEQUENCE sales_customer_id_seq;
CREATE TABLE customer (
    id NUMBER DEFAULT sales_customer_id_seq.NEXTVAL
);
```

### **Problem 2: Hierarchyid Type**
SQL Server's `hierarchyid` (organizational trees) isn't in Snowflake.

**Solution:** Cast to VARCHAR during extraction
```python
CAST(OrganizationNode AS VARCHAR(4000))
```

### **Problem 3: Geography Data**
SQL Server geography → Parquet thinks it's a complex object → Snowflake errors

**Solution:** Use CSV for this one table, convert geography to WKT text format

### **Problem 4: NULL Handling**
Pandas converts `None` → string `"None"` in some cases

**Solution:** Explicit NULL cleanup
```python
df = df.where(pd.notna(df), None)  # NaN → None
df = df.replace('None', None)       # String "None" → actual NULL
```

---

## 🧪 Validation & Quality Checks

**Automated checks in every script:**

```python
# Row count verification
sql_server_count = query("SELECT COUNT(*) FROM table")
snowflake_count = query("SELECT COUNT(*) FROM table")
assert sql_server_count == snowflake_count  # Must match!

# Data sampling
SELECT TOP 100 * FROM source  # Compare with Snowflake
```

**Final validation query:**
```sql
-- Proves migration success
SELECT 
    'Total Tables' AS metric, 
    COUNT(*) AS value 
FROM INFORMATION_SCHEMA.TABLES;
-- Result: 71 ✓
```

---

## 📈 Performance Notes

**Migration Speed:**
- Small tables (<1K rows): <1 second each
- Large tables (100K+ rows): 10-30 seconds each
- Total: ~3 minutes for 760K rows
- Throughput: ~6,500 rows/second

**Optimization Techniques:**
- Parquet columnar format (3x faster than CSV)
- Parallel COPY INTO (Snowflake auto-parallelizes)
- Batch processing (sorted by size, small→large)

---

## 🚧 Known Limitations & Workarounds

### **Spatial Data (Person.Address)**
**Issue:** SQL Server geography types  
**Workaround:** Separate CSV pipeline converts to WKT text  
**Production Fix:** Use Snowflake's native GEOGRAPHY type post-migration

### **Binary Data (ProductPhoto)**  
**Issue:** Large image blobs (VARBINARY)  
**Workaround:** Hex encoding converts to VARCHAR  
**Production Fix:** Store in cloud object storage (S3), reference in table

### **Custom User Types**
**Issue:** SQL Server has custom types like `Name`, `Flag`  
**Workaround:** Auto-converts to base types (both are NVARCHAR underneath)  

---

## 🎓 What You'll Learn

By running this project, you'll understand:

✅ How to **automate schema discovery** instead of manual documentation  
✅ How **data type mapping** works between different databases  
✅ Why **Parquet > CSV** for bulk data transfers  
✅ How **Snowflake staging** enables parallel bulk loading  
✅ How to handle **edge cases** (spatial, binary, hierarchical data)  
✅ Why **validation** is critical (row counts can silently mismatch!)  

---

## 📦 Installation & Setup

### Prerequisites

**Install these once:**

1. **Docker Desktop** ([download](https://www.docker.com/products/docker-desktop))
   - Why: Runs SQL Server without installing SQL Server on your machine
   
2. **Python 3.9+** ([download](https://www.python.org/downloads/))
   - Why: Powers all ETL scripts
   
3. **ODBC Driver 18** for SQL Server ([install guide](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))
   - Why: Lets Python connect to SQL Server

**For WSL users (recommended):**
```bash
# Install in WSL Ubuntu
sudo apt-get update
sudo apt-get install docker.io python3 python3-pip unixodbc unixodbc-dev
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

---

### Quick Setup (5 Commands)

```bash
# 1. Start SQL Server with AdventureWorks
docker-compose up -d                    # Pulls image, starts container
./setup/install_adventureworks.sh       # Downloads 200MB backup, restores DB

# 2. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate               # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
nano .env  # Add your Snowflake account details

# 4. You're ready! Run the migration (see Usage below)
```

---

## 🎮 Usage

### **Full Migration (Run in Order)**

```bash
# Activate Python environment (do this every time you open a new terminal)
source .venv/bin/activate

cd scripts

# PHASE 1: Discover what's in SQL Server
python 01_discover_schema.py
# → Output: ../data/discovery_report.json
# → Contains: All table structures, types, constraints

# PHASE 2: Convert SQL Server DDL → Snowflake DDL  
python 02_convert_schema.py
# → Output: ../snowflake_ddl/*.sql (5 files)
# → Logic: Uses config/type_mapping.json rules

# PHASE 3: Test Snowflake connection
python 03_test_snowflake_connection.py
# → Verifies: Credentials work, warehouse exists, permissions OK

# PHASE 4: Create empty schema in Snowflake
python 04_execute_ddl_snowflake.py
# → Creates: 6 schemas, 71 tables, 39 sequences
# → Note: Tables are empty at this point!

# PHASE 5: Migrate the data (bulk load)
python 05_migrate_data.py
# → Extracts: 70 tables from SQL Server
# → Loads: Via Parquet → Snowflake stage → COPY INTO
# → Time: ~2-3 minutes for 760K rows

# PHASE 6: Handle spatial data separately
python 06_load_person_address_csv.py
# → Special: Uses CSV for geography types
# → Loads: Person.Address table (19,614 rows)

# ✓ DONE! All 71 tables migrated
```

---

### **Understanding Each Script's Logic**

#### **Discovery Script Logic**
```python
# Connects to SQL Server
conn = pyodbc.connect("SQL Server connection string")

# Gets all user tables (not system tables)
tables = query("SELECT schema, table_name FROM sys.tables WHERE schema NOT IN ('sys')")

# For each table, get columns
for table in tables:
    columns = query("SELECT name, type, max_length FROM sys.columns WHERE table = ?", table)
    
# Gets constraints
pks = query("SELECT * FROM sys.indexes WHERE is_primary_key = 1")
fks = query("SELECT * FROM sys.foreign_keys")

# Saves everything to JSON for next scripts
save_to_json(discovery_report)
```

#### **Conversion Script Logic**
```python
# Reads discovery report
data = json.load('discovery_report.json')

# Loads conversion rules
type_map = json.load('type_mapping.json')

# Converts each table
for table in data['tables']:
    sql = "CREATE TABLE " + table.schema + "." + table.name + " ("
    
    for column in table['columns']:
        # Look up Snowflake type
        snowflake_type = type_map[column.sql_type]
        
        # Handle special cases
        if column.is_identity:
            # Create sequence instead
            create_sequence(schema, table, column)
        
        sql += column.name + " " + snowflake_type + ","
    
    sql += ");"
    save_to_file(sql)
```

#### **Migration Script Logic**
```python
# For each table in discovery report:
for table in tables:
    # 1. Extract from SQL Server
    query = build_query_with_type_casts(table)  # Handles hierarchyid, etc.
    df = pandas.read_sql(query, sql_connection)
    
    # 2. Clean NULLs
    df = df.where(pd.notna(df), None)
    
    # 3. Save as Parquet (compressed columnar format)
    df.to_parquet(f"{schema}_{table}.parquet")
    
    # 4. Upload to Snowflake stage
    snowflake.execute(f"PUT file://...parquet @stage")
    
    # 5. Bulk load
    snowflake.execute(f"COPY INTO {table} FROM @stage/{file} FILE_FORMAT=PARQUET")
    
    # 6. Verify
    source_count = sql_server.query("SELECT COUNT(*)")
    target_count = snowflake.query("SELECT COUNT(*)")
    assert source_count == target_count  # Must match!
```

---

## 🔍 Understanding the Type Mapping

**The `config/type_mapping.json` file contains rules like:**

```json
{
  "int": { "snowflake_type": "NUMBER", "precision": 38, "scale": 0 },
  "datetime": { "snowflake_type": "TIMESTAMP_NTZ" },
  "nvarchar": { "snowflake_type": "VARCHAR", "use_source_length": true },
  "hierarchyid": { "snowflake_type": "VARCHAR", "precision": 4000 }
}
```

**Why this matters:** SQL Server has ~40 data types, Snowflake has ~15. The mapper bridges this gap automatically.

**Special cases handled:**
- `NVARCHAR(100)` → `VARCHAR(50)` (SQL Server uses 2 bytes/char)
- `MONEY` → `NUMBER(19,4)` (Snowflake doesn't have MONEY type)
- `BIT` → `BOOLEAN` (direct equivalent)
- `IDENTITY` → `SEQUENCE` (different auto-increment mechanism)

---

## ⚠️ Common Issues & Solutions

### "Docker container not starting"
```bash
# Check if port 1433 is already in use
docker ps -a
docker-compose down -v  # Reset everything
docker-compose up -d
```

### "pyodbc module not found"
```bash
# Virtual environment not activated
source .venv/bin/activate
pip install -r requirements.txt
```

### "Snowflake connection timeout"
```bash
# Check .env file has correct account identifier
# Format: account.region (e.g., abc12345.us-east-1)
cat .env | grep SNOWFLAKE_ACCOUNT
```

### "Triple row counts in Snowflake"
```bash
# Tables loaded multiple times (use TRUNCATE or regenerate)
python 04_execute_ddl_snowflake.py  # Drops/recreates all tables
python 05_migrate_data.py           # Fresh migration
```

---

## 🤝 For Interviewers / Code Reviewers

**Key things to notice:**

1. **Automated type handling** - Not hardcoded mappings, uses JSON config
2. **Special type logic** - `get_column_list_with_cast()` handles hierarchyid, geography, time, varbinary
3. **Error handling** - Try/catch with detailed logging, continues on failure
4. **Validation framework** - Doesn't assume success, verifies row counts
5. **Separation of concerns** - Discovery → Convert → Migrate (each script does one thing)
6. **Real-world complexity** - Handles edge cases most tutorials skip

## 📚 Additional Resources

- [Snowflake Migration Best Practices](https://docs.snowflake.com/en/user-guide/migration)
- [AdventureWorks Schema Diagram](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure)
- [Parquet Format Specification](https://parquet.apache.org/docs/)

---

## 👤 Author

Built as a technical demonstration of enterprise database migration capabilities for Snowflake interview process.

**Skills demonstrated:** Python ETL, SQL optimization, cloud data warehousing, type system understanding, production engineering practices

---

**Questions?** This README should get you from zero to migrated in 15 minutes. If something's unclear, check `docs/SETUP_GUIDE.md` for detailed troubleshooting.