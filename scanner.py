import os
import hashlib
import sqlite3

class Scanner:
    def __init__(self, db_name='MacSafe.db'):
        self.db_name = db_name
        
    def create_table(self):
        # Create the BaselineExecutables table if it doesn't exist
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BaselineExecutables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                md5_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
    def scan_and_save(self, directory ='/usr/bin'):
        self.create_table()
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.access(file_path, os.X_OK):
                    md5_hash = self.calculate_md5(file_path)
                    self.insert_to_database(cursor, filename, file_path, md5_hash)
                    
        conn.commit()
        conn.close()
        
    def calculate_md5(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    
    def insert_to_database(self, cursor, name, path, md5_hash):
        cursor.execute('''
                            INSERT INTO BaselineExecutables (name, path, md5_hash)
                            VALUES (?, ?, ?)
            ''', (name, path, md5_hash))
        
if __name__ == "__main__":
    scanner = Scanner()
    scanner.scan_and_save()