from prettytable import PrettyTable 
import sqlite3 

class DatabaseViewer:
    def __init__(self, db_name="MacSafe.db", table_name="BaselineExecutables"):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def display_table_contents(self):
        # Fetch data from the database 
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        data = self.cursor.fetchall()
        
        # Get column names 
        column_names = [description[0] for description in self.cursor.description]
        
        # Create a PrettyTable
        table = PrettyTable(column_names)
        for row in data: 
            table.add_row(row)
        
        print(table)
        
    def close_connection(self):
        self.conn.close()
        
if __name__ == "__main__":
    viewer = DatabaseViewer()
    viewer.display_table_contents()
    viewer.close_connection()