import sqlite3
from tabulate import tabulate
from datetime import datetime
import os
from config import DATABASE_NAME, DATE_FORMAT, VALID_STATUSES, TABLE_FORMAT, CURRENCY_SYMBOL

def get_db_connection():
    """Create and return database connection"""
    if not os.path.exists(DATABASE_NAME):
        print(f"Database {DATABASE_NAME} not found. Please run 'python database.py' first.")
        return None
    return sqlite3.connect(DATABASE_NAME)

def validate_date(date_string):
    """Validate date format"""
    try:
        datetime.strptime(date_string, DATE_FORMAT)
        return True
    except ValueError:
        return False

def get_positive_float(prompt):
    """Get positive float input with validation"""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_positive_int(prompt):
    """Get positive integer input with validation"""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

# ---------------------- Listings ----------------------
def add_listing():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        
        title = input("House/Apartment Title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
            
        location = input("Location: ").strip()
        if not location:
            print("Location cannot be empty.")
            return
            
        price_per_day = get_positive_float("Price per day: ")
        
        host_name = input("Host name: ").strip()
        if not host_name:
            print("Host name cannot be empty.")
            return

        c.execute("INSERT INTO Listings (title, location, price_per_day, host_name) VALUES (?, ?, ?, ?)",
                  (title, location, price_per_day, host_name))
        conn.commit()
        print("Listing added successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def view_listings():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM Listings ORDER BY id")
        rows = c.fetchall()
        
        if rows:
            formatted_rows = []
            for row in rows:
                formatted_row = list(row)
                formatted_row[3] = f"{CURRENCY_SYMBOL}{row[3]:.2f}"
                formatted_rows.append(formatted_row)
            print(tabulate(formatted_rows, headers=["ID", "Title", "Location", "Price/day", "Host"], tablefmt=TABLE_FORMAT))
        else:
            print("No listings found.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# ---------------------- Bookings ----------------------
def create_booking():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        
        view_listings()
        
        listing_id = get_positive_int("Enter Listing ID to book: ")
        c.execute("SELECT id FROM Listings WHERE id = ?", (listing_id,))
        if not c.fetchone():
            print("Invalid listing ID.")
            return
        
        customer_name = input("Customer Name: ").strip()
        if not customer_name:
            print("Customer name cannot be empty.")
            return
        
        while True:
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            if validate_date(start_date):
                break
            print("Invalid date format. Please use YYYY-MM-DD.")
        
        while True:
            end_date = input("End Date (YYYY-MM-DD): ").strip()
            if validate_date(end_date):
                if end_date >= start_date:
                    break
                else:
                    print("End date must be after start date.")
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        c.execute("""
            SELECT COUNT(*) FROM Bookings 
            WHERE listing_id = ? AND status = 'Approved' 
            AND NOT (end_date < ? OR start_date > ?)
        """, (listing_id, start_date, end_date))
        
        if c.fetchone()[0] > 0:
            print("This listing is already booked for the selected dates.")
            return

        c.execute("INSERT INTO Bookings (listing_id, customer_name, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
                  (listing_id, customer_name, start_date, end_date, "Pending"))
        conn.commit()
        print("Booking created and is Pending approval!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def manage_bookings():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        
        c.execute("""
            SELECT B.id, L.title, B.customer_name, B.start_date, B.end_date, B.status 
            FROM Bookings B 
            JOIN Listings L ON B.listing_id = L.id 
            ORDER BY B.id
        """)
        rows = c.fetchall()

        if not rows:
            print("No bookings found.")
            return

        print(tabulate(rows, headers=["Booking ID", "Listing", "Customer", "Start", "End", "Status"], tablefmt=TABLE_FORMAT))

        booking_id = get_positive_int("Enter Booking ID to update: ")
        
        c.execute("SELECT status FROM Bookings WHERE id = ?", (booking_id,))
        result = c.fetchone()
        if not result:
            print("Invalid booking ID.")
            return
        
        current_status = result[0]
        if current_status != "Pending":
            print(f"Booking is already {current_status}. Only Pending bookings can be updated.")
            return
        
        while True:
            status = input("Enter new status (Approved/Rejected): ").strip().capitalize()
            if status in VALID_STATUSES[1:]:
                break
            print("Invalid status. Must be Approved or Rejected.")

        c.execute("UPDATE Bookings SET status = ? WHERE id = ?", (status, booking_id))
        conn.commit()
        print(f"Booking {booking_id} updated to {status}!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def view_earnings():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        
        c.execute("""
            SELECT L.id, L.title, L.host_name,
                   COALESCE(SUM((julianday(B.end_date) - julianday(B.start_date) + 1) * L.price_per_day), 0) AS earnings
            FROM Listings L
            LEFT JOIN Bookings B ON L.id = B.listing_id AND B.status = 'Approved'
            GROUP BY L.id, L.title, L.host_name
            ORDER BY earnings DESC
        """)
        rows = c.fetchall()
        
        if rows:
            formatted_rows = []
            total_earnings = 0
            for row in rows:
                formatted_row = list(row)
                earnings = row[3] if row[3] else 0
                formatted_row[3] = f"{CURRENCY_SYMBOL}{earnings:.2f}"
                total_earnings += earnings
                formatted_rows.append(formatted_row)
            
            print(tabulate(formatted_rows, headers=["Listing ID", "Title", "Host", "Earnings"], tablefmt=TABLE_FORMAT))
            print(f"\nTotal Earnings: {CURRENCY_SYMBOL}{total_earnings:.2f}")
        else:
            print("No earnings data found.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def menu():
    print("Welcome to House Rental CLI!")
    print("Make sure you have run 'python database.py' to set up the database.\n")
    
    while True:
        try:
            print("\n--- House Rental CLI ---")
            print("1. Add Listing")
            print("2. View All Listings")
            print("3. Create Booking")
            print("4. Approve/Reject Booking")
            print("5. View Earnings Report")
            print("6. Exit")
            
            choice = input("Select an option (1-6): ").strip()

            if choice == "1":
                add_listing()
            elif choice == "2":
                view_listings()
            elif choice == "3":
                create_booking()
            elif choice == "4":
                manage_bookings()
            elif choice == "5":
                view_earnings()
            elif choice == "6":
                print("Thank you for using House Rental CLI. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\nExiting House Rental CLI. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    menu()