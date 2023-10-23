import sqlite3

class Database:
    def __init__(self, db_name='MacSafe.db'):
        self.db_name = db_name
    
    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create the BaselineExecutables table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BaselineExecutables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                md5_hash TEXT
            )
        ''')
        
        conn.commit()
        
        # Create the BaselineAccounts table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BaselineAccounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                date_created TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        
        # Create the TrustedConnections table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TrustedConnections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                IPAddress TEXT UNIQUE NOT NULL
            )
        ''')
        
        conn.commit()
        
        # Create the Connections table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Protocol TEXT NOT NULL,
                Local_Address TEXT NOT NULL,
                Local_Port INTEGER NOT NULL,
                Foreign_Address TEXT,
                Foreign_Port INTEGER,
                State TEXT NOT NULL
                
            )
        ''')
        
if __name__ == "__main__":
    database = Database()
    database.create_tables()