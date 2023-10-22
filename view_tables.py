from prettytable import PrettyTable 
import sqlite3 

class DatabaseViewer:
    def __init__(self, db_name="MacSafe.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def show_tables(self):
        db_name = self.db_name
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Query to retrieve all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        tables = cursor.fetchall()
        if tables:
            print("Tables in the database:")
            print("-------------------------")
            for table in tables:
                print(table[0])
            print("-------------------------")
        else:
            print("No tables found in the database")
     
    def display_table_contents(self):
        # Fetch data from the database 
        self.show_tables()
        table_name = input("What table would you like to view?")
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()
        
        # Get column names 
        column_names = [description[0] for description in self.cursor.description]
        
        # Create a PrettyTable
        table = PrettyTable(column_names)
        for row in data: 
            table.add_row(row)
        
        print(table)
        
    def display_trusted_connections(self):
        db_name = self.db_name
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Query TrustedConnections and retrieve all records
        cursor.execute("SELECT * FROM TrustedConnections")
        
        rows = cursor.fetchall()
        
        table = PrettyTable(["ID", "IP Address"])
        
        for row in rows:
            table.add_row([row[0],row[1]])
        
        print(table)
        
    def close_connection(self):
        self.conn.close()
        
if __name__ == "__main__":
    viewer = DatabaseViewer()
    viewer.display_table_contents()
    viewer.close_connection()