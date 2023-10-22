from ui import App
from scanner import Scanner
from database import Database
import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


# Create an instance of the scanner class
scanner = Scanner()
app = App()
database = Database()

# Create a flag to control the exit
exit_flag = threading.Event()

def run_scanner(db_name="MacSafe.db"):
    # Create a SQLAlchemy engine and session
    engine = create_engine(f"sqlite:///{db_name}", poolclass=QueuePool)
    Session = sessionmaker(bind=engine)

    while not exit_flag.is_set():    
        # Create a new session for each loop iteration
        session = Session()
        try:
            scanner.scan_and_save(directory='/usr/bin')
            users = scanner.get_macos_user_accounts()
            scanner.insert_user_accounts_to_db(users)
            scanner.capture_and_store_connection_data()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error in scanner:{e}")
        finally:
            session.close()
        
        time.sleep(600)
    # Start the scanner in a separate thread so that it starts and runs at the same time as the UI which is when the script is run
scanner_thread = threading.Thread(target=run_scanner)
scanner_thread.daemon = True
scanner_thread.start()

def main():
    print("Welcome to MC-Hammer")
    
    # Automatically run the UI
    app.run()
    
    # Set the exit flag to signal the scanner to exit
    
    exit_flag.set()
    
if __name__ == "__main__":
    database.create_tables()
    scanner.add_trusted_connections()
    main()
    