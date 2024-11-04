import psycopg2
import time
from datetime import datetime
import os
import psutil
from tabulate import tabulate as tabulate_func
import threading
import queue

class PostgresMonitor:
    def __init__(self):
        self.connection_params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "Gelules123!",
            "host": "localhost",
            "port": "5432"
        }
        self.stop_event = threading.Event()
        self.metrics_queue = queue.Queue()

    def get_db_stats(self):
        """Get database statistics"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    # Database size
                    cur.execute("""
                        SELECT pg_size_pretty(pg_database_size('postgres'));
                    """)
                    db_size = cur.fetchone()[0]

                    # Connection count
                    cur.execute("""
                        SELECT count(*) FROM pg_stat_activity;
                    """)
                    connections = cur.fetchone()[0]

                    # Cache hit ratio
                    cur.execute("""
                        SELECT 
                            CASE WHEN sum(heap_blks_hit) + sum(heap_blks_read) = 0 
                                 THEN '0.00%'
                                 ELSE round(sum(heap_blks_hit) * 100.0 / 
                                          (sum(heap_blks_hit) + sum(heap_blks_read)), 2)::text || '%'
                            END
                        FROM pg_statio_user_tables;
                    """)
                    cache_hit_ratio = cur.fetchone()[0]

                    # Transaction stats
                    cur.execute("""
                        SELECT 
                            xact_commit,
                            xact_rollback,
                            tup_inserted,
                            tup_updated,
                            tup_deleted
                        FROM pg_stat_database 
                        WHERE datname = 'postgres';
                    """)
                    stats = cur.fetchone()

                    return {
                        'db_size': db_size,
                        'connections': connections,
                        'cache_hit_ratio': cache_hit_ratio,
                        'commits': stats[0],
                        'rollbacks': stats[1],
                        'inserts': stats[2],
                        'updates': stats[3],
                        'deletes': stats[4]
                    }
        except Exception as e:
            return f"Error: {str(e)}"

    def get_system_stats(self):
        """Get system statistics"""
        try:
            # Find PostgreSQL process
            postgres_proc = None
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                if 'postgres' in proc.name().lower() and 'postmaster' not in proc.name().lower():
                    postgres_proc = proc
                    break

            if postgres_proc:
                mem_info = postgres_proc.memory_info()
                cpu_percent = postgres_proc.cpu_percent(interval=1.0)
                
                return {
                    'memory_used': f"{mem_info.rss / (1024*1024):.1f} MB",
                    'cpu_percent': f"{cpu_percent:.1f}%",
                    'threads': postgres_proc.num_threads()
                }
            return "PostgreSQL process not found"
        except Exception as e:
            return f"Error: {str(e)}"

    def format_metrics(self, metrics):
        """Format metrics for display"""
        output = []
        
        # Header
        output.append("\n=== PostgreSQL Performance Monitor ===")
        output.append(f"Timestamp: {metrics['timestamp']}\n")
        
        # Database Stats
        output.append("Database Statistics:")
        output.append(f"├─ Size: {metrics['db_size']}")
        output.append(f"├─ Active Connections: {metrics['connections']}")
        output.append(f"└─ Cache Hit Ratio: {metrics['cache_hit_ratio']}\n")
        
        # System Stats
        output.append("System Resource Usage:")
        output.append(f"├─ Memory: {metrics['memory_used']}")
        output.append(f"├─ CPU: {metrics['cpu_percent']}")
        output.append(f"└─ Threads: {metrics['threads']}\n")
        
        # Transaction Stats
        output.append("Transaction Statistics:")
        output.append(f"├─ Commits: {metrics['commits']}")
        output.append(f"├─ Rollbacks: {metrics['rollbacks']}")
        output.append(f"├─ Inserts: {metrics['inserts']}")
        output.append(f"├─ Updates: {metrics['updates']}")
        output.append(f"└─ Deletes: {metrics['deletes']}\n")
        
        return "\n".join(output)

    def monitor_metrics(self):
        """Collect metrics periodically"""
        while not self.stop_event.is_set():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_stats = self.get_db_stats()
            sys_stats = self.get_system_stats()
            
            if isinstance(db_stats, dict) and isinstance(sys_stats, dict):
                metrics = {
                    'timestamp': timestamp,
                    **db_stats,
                    **sys_stats
                }
                self.metrics_queue.put(metrics)
            
            time.sleep(5)  # Collect metrics every 5 seconds

    def display_metrics(self):
        """Display collected metrics"""
        while not self.stop_event.is_set():
            try:
                metrics = self.metrics_queue.get(timeout=1)
                
                # Clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Display formatted metrics
                print(self.format_metrics(metrics))
                print("Press Ctrl+C to stop monitoring")
                
            except queue.Empty:
                continue

def main():
    print("\n=== PostgreSQL Performance Monitor ===")
    print("Starting monitoring (Press Ctrl+C to stop)...")
    
    monitor = PostgresMonitor()
    
    # Start metrics collection in a separate thread
    metrics_thread = threading.Thread(target=monitor.monitor_metrics)
    metrics_thread.daemon = True
    metrics_thread.start()
    
    try:
        # Display metrics in main thread
        monitor.display_metrics()
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop_event.set()
        metrics_thread.join(timeout=1)
        print("Monitor stopped")

if __name__ == "__main__":
    main()