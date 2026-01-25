#!/bin/bash
set -e

SQL_PASSWORD="YourStrong@Passw0rd"
CONTAINER_NAME="adventureworks-sqlserver"
BACKUP_FILE="AdventureWorks2022.bak"
BACKUP_URL="https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2022.bak"

echo "=== AdventureWorks Setup Script ==="

# Check container
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "ERROR: Container not running!"
    exit 1
fi
echo "✓ Container is running"

# Download
if [ ! -f "./setup/$BACKUP_FILE" ]; then
    curl -L -o "./setup/$BACKUP_FILE" "$BACKUP_URL"
    echo "✓ Download complete"
else
    echo "✓ Backup file already exists"
fi

# Copy
docker cp "./setup/$BACKUP_FILE" $CONTAINER_NAME:/var/opt/mssql/data/
echo "✓ File copied"

# Restore - FIXED PATH
docker exec $CONTAINER_NAME /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "$SQL_PASSWORD" -C \
    -Q "RESTORE DATABASE AdventureWorks2022 FROM DISK='/var/opt/mssql/data/$BACKUP_FILE' WITH MOVE 'AdventureWorks2022' TO '/var/opt/mssql/data/AdventureWorks2022.mdf', MOVE 'AdventureWorks2022_log' TO '/var/opt/mssql/data/AdventureWorks2022_log.ldf', REPLACE"

# Verify - FIXED PATH  
docker exec $CONTAINER_NAME /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "$SQL_PASSWORD" -C \
    -Q "SELECT name FROM sys.databases WHERE name = 'AdventureWorks2022'"

echo "✓ Setup Complete!"