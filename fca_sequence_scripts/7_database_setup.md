# PostgreSQL Setup Guide for Windows

## 1. Install PostgreSQL

1. Download PostgreSQL for Windows from the official website:
   - Visit https://www.postgresql.org/download/windows/
   - Choose the latest version of PostgreSQL installer

2. Run the installer:
   - Keep note of the password you set for the postgres user
   - Default port: 5432
   - Install all offered components

## 2. Verify Installation

1. Open Command Prompt and add PostgreSQL to your PATH:
```cmd
set PATH=%PATH%;C:\Program Files\PostgreSQL\{version}\bin
```

2. Test PostgreSQL:
```cmd
psql --version
```

## 3. Create Database

1. Open Command Prompt and connect to PostgreSQL:
```cmd
psql -U postgres
```

2. Create the database:
```sql
CREATE DATABASE fca_categorization;
```

3. Verify the database was created:
```sql
\l
```

4. Exit psql:
```sql
\q
```

## 4. Configure Environment

1. Update .env file with your PostgreSQL credentials:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost/fca_categorization
```

## 5. Common Issues

### Connection Refused Error
If you see "connection refused" error:
1. Check if PostgreSQL service is running:
   - Open Services (services.msc)
   - Find "postgresql-x64-{version}"
   - Ensure it's running
   - If not, start it

2. Verify PostgreSQL is listening:
   - Open Command Prompt as Administrator
   - Run: `netstat -an | find "5432"`
   - Should see "LISTENING" on port 5432

### Password Authentication Failed
If you see authentication errors:
1. Verify your password in .env matches what you set during installation
2. Try connecting with psql to confirm credentials:
```cmd
psql -U postgres -d fca_categorization
```

## 6. Next Steps

After PostgreSQL is running and accessible:
1. Run database migrations:
```cmd
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

2. Verify database tables:
```cmd
psql -U postgres -d fca_categorization
\dt
