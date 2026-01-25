## 🚀 Full Migration (Copy-Paste)
```bash
# Setup (one-time)
docker-compose up -d
./setup/install_adventureworks.sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Migration (run in order)
cd scripts
python 01_discover_schema.py
python 02_convert_schema.py
python 03_test_snowflake_connection.py
python 04_execute_ddl_snowflake.py
python 05_migrate_data.py
python 06_load_person_address_csv.py
```

## 🔧 Daily Commands
```bash
# Start/stop SQL Server
docker-compose up -d
docker-compose down

# Activate Python
source .venv/bin/activate

# Check status
docker ps
docker logs adventureworks-sqlserver


```
## 🧹 Reset
```bash
docker-compose down -v              # Delete everything
rm -rf data/ snowflake_ddl/ .venv   # Clean outputs
```
