import ui
import threading
from scanner import Scanner
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


# Create an instance of the scanner class
scanner = Scanner()

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
    ui.main()
    
    # Set the exit flag to signal the scanner to exit
    
    exit_flag.set()
    
if __name__ == "__main__":
    main()
    