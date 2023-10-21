from blessed import Terminal 
import os
from scanner import Scanner
from view_tables import DatabaseViewer

# Initialize the terminal 
term = Terminal()

# Dummy data for trusted connecitons and alerts 
trusted_connections = ["127.0.0.1", " 192.168.1.1"]

alerts = [ "Alert 1: Suspicious activity detected", "Alert 2: High CPU usage" ]

def clear_screen():
    print(term.clear())

def start_scan():
    try:
        scanner = Scanner()
        scanner.scan_and_save()
        print("Scan complete")        
    except Exception as e:
        print(f"Eror while starting scan {str(e)}")

def view_tables():
    clear_screen()
    print("Viewing Tables")
    db_viewer = DatabaseViewer()
    db_viewer.display_table_contents()
    db_viewer.close_connection()
    
    input("\nPress Enter to continue")
    
def add_trusted_connection():
    conn = input("Enter a trusted connection IP address in IPv4 format")
    if conn:
        trusted_connections.append(conn)
        print("Connection added")
        
def remove_trusted_connection():
    print("trusted Connections:")
    for i, conn in enumerate(trusted_connections):
        print(f"{i +1}. {conn}")
        
        try:
            choice = int(input("Enter the number to remove (0 to cancel): "))
            if 1 <= choice <= len(trusted_connections):
                removed_conn = trusted_connections.pop(choice - 1)
                print(f"Removed {removed_conn}")
            elif choice != 0:
                print("Invalid choice")
        except ValueError:
            print("Invalid input. Please enter a number.")

def alerts_menu():
    clear_screen()
    print("Alerts")
    for alert in alerts:
        input("\nPress Enter to continue")
        
def main():
    while True:
        print("-----------------------------------------------")
        print("Welcome to MC-Hammer => 'You Can't Touch This!")
        print("Options")
        print("------------------------------------------------")
        print("1. Start Scan")
        print("2. View Tables")
        print("3. Add Trusted Connection")
        print("4. Remove Trusted Connection")
        print("5. Alerts")
        print("6. Exit")
        print("-------------------------------------------------")
        
        choice = input("Enter your choice: ")
        
        if choice =="1":
            start_scan()
        elif choice =="2":
            view_tables()
        elif choice =="3":
            add_trusted_connection()
        elif choice == "4":
            remove_trusted_connection()
        elif choice =="5":
            alerts_menu()
        elif choice =="6":
            clear_screen()
            print("Goodbye!")
            break 
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()
        