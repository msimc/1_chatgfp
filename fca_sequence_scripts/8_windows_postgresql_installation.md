# PostgreSQL Installation Guide for Windows

## Step-by-Step Installation

1. **Download PostgreSQL**
   - Go to https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
   - Download PostgreSQL 15.x for Windows x86-64
   - Current direct link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows

2. **Run the Installer**
   - Double-click the downloaded installer
   - Click "Next" through the installation wizard
   - Set a password for the postgres user (IMPORTANT: Remember this password!)
   - Keep the default port (5432)
   - Keep the default locale

3. **Installation Options**
   Select the following components:
   - PostgreSQL Server
   - pgAdmin 4
   - Command Line Tools
   - Stack Builder

4. **Post-Installation**
   - Launch pgAdmin 4 from the Start Menu
   - When prompted, enter the password you set during installation
   - In the Object Explorer (left panel), expand "Servers"
   - Right-click "PostgreSQL" and select "Connect Server"
   - Enter your password when prompted

5. **Create Database**
   Using pgAdmin 4:
   - Right-click "Databases"
   - Select "Create" > "Database"
   - Enter "fca_categorization" as the database name
   - Click "Save"

## Verify Installation

1. **Check PostgreSQL Service**
   - Press Win + R
   - Type "services.msc" and press Enter
   - Look for "postgresql-x64-15" (or your version)
   - Status should be "Running"
   - Startup type should be "Automatic"

2. **Test Command Line Access**
   Open Command Prompt and try:
   ```cmd
   psql -U postgres -d postgres
   ```
   Enter your password when prompted.

## Update Project Configuration

1. **Update .env File**
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost/fca_categorization
   ```
   Replace "your_password" with the password you set during installation.

2. **Test Database Connection**
   ```cmd
   psql -U postgres -d fca_categorization
   ```
   If successful, you should see:
   ```
   psql (15.x)
   Type "help" for help.

   fca_categorization=#
   ```

## Troubleshooting

### Common Issues

1. **Service Not Running**
   - Open Services (services.msc)
   - Find postgresql-x64-15
   - Right-click and select "Start"

2. **Port Conflict**
   - Check if another service is using port 5432:
   ```cmd
   netstat -ano | findstr :5432
   ```

3. **Connection Refused**
   - Verify service is running
   - Check pg_hba.conf allows local connections
   - Ensure firewall isn't blocking connections

4. **Password Authentication Failed**
   - Double-check password in .env
   - Try connecting with pgAdmin 4 first
   - Reset password if necessary

### Getting Help

1. **View PostgreSQL Logs**
   - Open pgAdmin 4
   - Server > View Log

2. **Check Configuration**
   - Location: C:\Program Files\PostgreSQL\15\data
   - Files to check:
     - postgresql.conf
     - pg_hba.conf

## Next Steps After Installation

1. **Create Database**
   ```sql
   CREATE DATABASE fca_categorization;
   ```

2. **Run Migrations**
   ```cmd
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

3. **Verify Tables**
   ```sql
   \c fca_categorization
   \dt
   ```

## Maintenance

1. **Backup Database**
   ```cmd
   pg_dump -U postgres -d fca_categorization > backup.sql
   ```

2. **Monitor Space**
   ```sql
   SELECT pg_size_pretty(pg_database_size('fca_categorization'));
   ```

3. **Regular Tasks**
   - Monitor disk space
   - Check error logs
   - Update passwords regularly
   - Keep PostgreSQL updated
