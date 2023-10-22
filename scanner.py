import os
import hashlib
import sqlite3
import ipaddress
import subprocess
import socket
import psutil
from view_tables import DatabaseViewer
from datetime import datetime

class Scanner:
    def __init__(self, db_name='MacSafe.db'):
        self.db_name = db_name
        
    def scan_and_save(self, directory ='/usr/bin'):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.access(file_path, os.X_OK):
                    md5_hash = self.calculate_md5(file_path)
                    self.insert_to_database(cursor, filename, file_path, md5_hash)
                    
        conn.commit()
        
    def calculate_md5(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    
    def insert_to_database(self, cursor, name, path, md5_hash, db_name="MacSafe.db"):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
                            INSERT INTO BaselineExecutables (name, path, md5_hash)
                            VALUES (?, ?, ?)
            ''', (name, path, md5_hash))
        conn.commit()
        
    def get_macos_user_accounts(self):
        # Get a list of user account names on macOS
        users = os.listdir('/Users')
        return users

    def insert_user_accounts_to_db(self, users, db_name='MacSafe.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        for username in users:
            # Get the account creation date in DD-MM-YYYY HH:MM:SS format
            user_path = os.path.join('/Users', username)
            creation_timestamp = os.path.getctime(user_path)
            creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%d-%m-%Y %H:%M:%S')
            
            cursor.execute('''
                           INSERT INTO BaselineAccounts (username, date_created)
                           VALUES (?, ?)
            ''', (username, creation_date))
            
            conn.commit()
            
    def add_trusted_connections(self, db_name='MacSafe.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Get user input for the trusted IP addresses
        ip_input = input("Enter the IPv4 address you would like to add: ")
        
        try:
            ipaddress.IPv4Address(ip_input)
        except ValueError:
            print("That's not a valid IPv4 address")
            return
        
        # Insert into database 
        try:
            cursor.execute("INSERT INTO TrustedConnections (IPAddress) VALUES (?)", (ip_input,))
            conn.commit()
            print(f"Added {ip_input} to TrustedConnections!")
        except sqlite3.IntegrityError:
            print(f"{ip_input} is already in TrustedConnections!")
            
    def remove_trusted_connection(self):
        db_viewer = DatabaseViewer()
        db_viewer.display_trusted_connections()
        
        # Get user input
        try:
            id_to_remove = int(input("Enter he ID of the record you want to remove: "))
        except ValueError:
                print("Please enter a valid integer for the ID")
                return
        
        db_name = self.db_name    
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Delete the record 
        cursor.execute("DELETE FROM TrustedConnections WHERE id = ?", (id_to_remove,))

        if cursor.rowcount > 0:
            print(f"Removed record with ID {id_to_remove} from TrustedConnections.")
        else:
            print(f"No record found with ID {id_to_remove}.")
        
        conn.commit()
        
    def capture_and_store_connection_data(self):
        connections = psutil.net_connections(kind='inet')
        
        conn_data = []
        seen = set()
        for conn in connections: 
            if conn.family == socket.AF_INET:
                protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
            local_address, local_port = conn.laddr
            foreign_address, foreign_port = conn.raddr if conn.raddr else (None, None)
            state = conn.status 
            
            data_tuple = (protocol, local_address, local_port, foreign_address, foreign_port, state)
            
            unwanted_tuple = ('UDP', '0.0.0.0', 0, None, None, 'NONE')
            if data_tuple != unwanted_tuple and data_tuple not in seen:
                conn_data.append(data_tuple)
                seen.add(data_tuple)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.executemany('''
            INSERT INTO Connections (Protocol, Local_Address, Local_Port, Foreign_Address, Foreign_Port, State)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', conn_data)
        
        conn.commit()
        
if __name__ == "__main__":
    scanner = Scanner()
    scanner.scan_and_save()