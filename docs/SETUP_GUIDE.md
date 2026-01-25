# AdventureWorks to Snowflake Migration - Setup Guide

## 📋 Prerequisites Installation

### 1. Install Docker Desktop

**Windows:**
1. Download from: https://www.docker.com/products/docker-desktop
2. Run installer and follow prompts
3. Restart computer when prompted
4. Open Docker Desktop to verify installation
5. In terminal, run: `docker --version` (should show version number)

**Mac:**
1. Download from: https://www.docker.com/products/docker-desktop
2. Drag Docker.app to Applications folder
3. Open Docker from Applications
4. In terminal, run: `docker --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
docker --version
```

### 2. Install Python 3.9+

**Windows:**
1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: `python --version` in Command Prompt

**Mac:**
```bash
# Using Homebrew
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version
```

### 3. Install ODBC Driver for SQL Server

**Windows:**
1. Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
2. Choose "ODBC Driver 18 for SQL Server"
3. Run installer with default settings

**Mac:**
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql18 mssql-tools18
```

**Linux (Ubuntu/Debian):**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

---

## 🚀 Project Setup

### Step 1: Download Project Files

1. Download all project files to a folder, e.g., `C:\Projects\adventureworks-migration`
2. Open terminal/command prompt in this folder

**Verify structure:**
```
adventureworks-migration/
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── setup/
│   └── install_adventureworks.sh
└── scripts/
    └── 01_discover_schema.py
```

### Step 2: Create Python Virtual Environment

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (~2-3 minutes).

---

## 🗄️ SQL Server Setup

### Step 1: Start SQL Server Container

```bash
docker-compose up -d
```

**What this does:**
- Downloads SQL Server 2022 image (~1.5 GB, first time only)
- Creates and starts container
- Exposes SQL Server on port 1433

**Verify it's running:**
```bash
docker ps
```
You should see `adventureworks-sqlserver` in the list.

**Wait for startup (important!):**
```bash
# Check logs until you see "SQL Server is now ready for client connections"
docker logs adventureworks-sqlserver -f
```
Press `Ctrl+C` to exit logs. Wait about 30 seconds after startup.

### Step 2: Install AdventureWorks Database

**Mac/Linux:**
```bash
chmod +x setup/install_adventureworks.sh
./setup/install_adventureworks.sh
```

**Windows (Git Bash recommended) or use PowerShell version:**

Create `setup/install_adventureworks.ps1`:
```powershell
# PowerShell version of setup script
$SQL_PASSWORD = "YourStrong@Passw0rd"
$CONTAINER_NAME = "adventureworks-sqlserver"
$BACKUP_FILE = "AdventureWorks2022.bak"
$BACKUP_URL = "https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2022.bak"

Write-Host "=== AdventureWorks Setup Script ===" -ForegroundColor Green

# Download backup
if (-not (Test-Path "setup\$BACKUP_FILE")) {
    Write-Host "Downloading backup file..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $BACKUP_URL -OutFile "setup\$BACKUP_FILE"
}

# Copy to container
Write-Host "Copying backup to container..." -ForegroundColor Yellow
docker cp "setup\$BACKUP_FILE" ${CONTAINER_NAME}:/var/opt/mssql/data/

# Restore database
Write-Host "Restoring database..." -ForegroundColor Yellow
docker exec $CONTAINER_NAME /opt/mssql-tools/bin/sqlcmd `
    -S localhost -U sa -P $SQL_PASSWORD `
    -Q "RESTORE DATABASE AdventureWorks2022 FROM DISK='/var/opt/mssql/data/$BACKUP_FILE' WITH MOVE 'AdventureWorks2022' TO '/var/opt/mssql/data/AdventureWorks2022.mdf', MOVE 'AdventureWorks2022_log' TO '/var/opt/mssql/data/AdventureWorks2022_log.ldf', REPLACE"

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
```

Then run:
```powershell
.\setup\install_adventureworks.ps1
```

**Expected output:**
```
✓ Container is running
✓ Download complete
✓ File copied
✓ Database restored
```

### Step 3: Verify Database Installation

**Test connection:**
```bash
docker exec adventureworks-sqlserver /opt/mssql-tools/bin/sqlcmd \
    -S localhost -U sa -P YourStrong@Passw0rd \
    -Q "SELECT name FROM sys.databases"
```

You should see `AdventureWorks2022` in the list.

---

## 🔍 Run Schema Discovery (Phase 1 Complete!)

### Execute Discovery Script

```bash
cd scripts
python 01_discover_schema.py
```

**Expected output:**
```
=== Starting Schema Discovery ===

✓ Connected to AdventureWorks2022
✓ Found 71 tables
✓ Column metadata complete
✓ Found 68 primary keys
✓ Found 90 foreign keys
✓ Found 20 views
✓ Found 11 stored procedures
✓ Discovery complete
✓ Report saved to: ../data/discovery_report.json

==================================================
DISCOVERY SUMMARY
==================================================
Database: AdventureWorks2022
Tables: 71
Total Rows: 294,451
Views: 20
Stored Procedures: 11
Primary Keys: 68
Foreign Keys: 90
==================================================
```

### View Discovery Report

Open `data/discovery_report.json` in any text editor or JSON viewer.

---

## ✅ Phase 1 Complete!

You now have:
- ✅ SQL Server running in Docker
- ✅ AdventureWorks database installed
- ✅ Complete schema inventory in JSON format
- ✅ Python environment configured

---

## 🛠️ Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon":**
- Ensure Docker Desktop is running
- Restart Docker Desktop

**Port 1433 already in use:**
- Change port in `docker-compose.yml`: `"1434:1433"`
- Update scripts to use `localhost,1434`

### Python Issues

**"pyodbc not found":**
```bash
pip install --upgrade pip
pip install pyodbc
```

**"Can't open lib 'ODBC Driver 18'":**
- Reinstall ODBC driver (see prerequisites)
- Try changing driver in script to "ODBC Driver 17 for SQL Server"

### SQL Server Issues

**Connection timeout:**
- Wait 60 seconds after `docker-compose up`
- Check logs: `docker logs adventureworks-sqlserver`

**Login failed:**
- Verify password: `YourStrong@Passw0rd` (case-sensitive)
- Check SA_PASSWORD in docker-compose.yml

---

## 🧹 Cleanup Commands

**Stop SQL Server:**
```bash
docker-compose down
```

**Remove all data (start fresh):**
```bash
docker-compose down -v
```

**Deactivate Python environment:**
```bash
deactivate
```

---

## 📞 Next Steps

Once Phase 1 is complete, we'll move to:
- **Phase 2:** Snowflake account setup
- **Phase 3:** Schema conversion (SQL Server → Snowflake DDL)
- **Phase 4:** Data migration with Parquet
- **Phase 5:** Validation

---

## 📝 Notes

- Default password: `YourStrong@Passw0rd` (change in production!)
- SQL Server uses ~2GB RAM
- Discovery report is reusable for documentation
- Keep `discovery_report.json` for later phases