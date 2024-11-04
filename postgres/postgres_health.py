import psycopg2
import psutil
import os
import subprocess
import time
from datetime import datetime

class PostgresHealthManager:
    def __init__(self):
        self.connection_params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "Gelules123!",
            "host": "localhost",
            "port": "5432"
        }
        self.bin_dir = r"C:\Program Files\PostgreSQL\17\bin"
        self.data_dir = r"C:\Program Files\PostgreSQL\17\data"

    def start_postgres_direct(self):
        """Start PostgreSQL using pg_ctl directly"""
        try:
            print("Starting PostgreSQL directly with pg_ctl...")
            
            # Kill any existing PostgreSQL processes first
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'postgres' in proc.info['name'].lower():
                        proc.kill()
                        time.sleep(1)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Start PostgreSQL
            pg_ctl = os.path.join(self.bin_dir, "pg_ctl.exe")
            cmd = [
                pg_ctl,
                "-D", self.data_dir,
                "start",
                "-w",  # Wait for startup
                "-t", "60",  # 60 second timeout
                "-l", os.path.join(self.data_dir, "startup.log")
            ]
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=70)  # Include some extra time
            
            print(f"Start command output: {result.stdout}")
            if result.stderr:
                print(f"Start command errors: {result.stderr}")
            
            # Check if startup was successful
            time.sleep(2)
            return self.check_connection()
            
        except subprocess.TimeoutExpired:
            print("Timeout while starting PostgreSQL")
            return False
        except Exception as e:
            print(f"Error starting PostgreSQL: {str(e)}")
            return False

    def check_connection(self, timeout=5):
        """Test PostgreSQL connection with timeout"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with psycopg2.connect(**self.connection_params, 
                                    connect_timeout=3) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT 1")
                        return True
            except psycopg2.OperationalError:
                time.sleep(1)
                continue
            except Exception as e:
                print(f"Connection error: {str(e)}")
                return False
        return False

    def check_startup_log(self):
        """Check PostgreSQL startup log for errors"""
        log_file = os.path.join(self.data_dir, "startup.log")
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    last_lines = f.readlines()[-10:]  # Get last 10 lines
                    print("\nRecent startup log entries:")
                    for line in last_lines:
                        print(line.strip())
            except Exception as e:
                print(f"Error reading log: {str(e)}")

    def manage_health(self):
        """Main health management function"""
        print("\n=== PostgreSQL Health Manager ===")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check if PostgreSQL is accepting connections
        if not self.check_connection(timeout=3):
            print("\n❌ PostgreSQL is not running or not accepting connections")
            response = input("Would you like to start PostgreSQL? (y/n): ")
            
            if response.lower() == 'y':
                if self.start_postgres_direct():
                    print("✅ PostgreSQL started successfully")
                else:
                    print("❌ Failed to start PostgreSQL")
                    self.check_startup_log()
                    print("\nTroubleshooting steps:")
                    print("1. Check startup.log for errors")
                    print("2. Verify data directory permissions")
                    print("3. Try starting manually:")
                    print(f'   cd "{self.bin_dir}"')
                    print(f'   .\\pg_ctl.exe -D "{self.data_dir}" start')
                    return False
        
        # If we get here, PostgreSQL should be running
        print("\nChecking PostgreSQL status...")
        if self.check_connection():
            print("✅ PostgreSQL is running and accepting connections")
            return True
        else:
            print("❌ Cannot connect to PostgreSQL")
            return False

def main():
    manager = PostgresHealthManager()
    manager.manage_health()

if __name__ == "__main__":
    main()