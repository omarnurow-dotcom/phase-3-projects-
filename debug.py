#!/usr/bin/env python3
import sqlite3
from tabulate import tabulate
from config import DATABASE_NAME

def debug_database():
    """Debug database structure and data"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        print("=== DATABASE DEBUG INFO ===\n")
        
        # Show all tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        print(f"Tables: {[t[0] for t in tables]}\n")
        
        # Show Listings table info
        print("--- LISTINGS TABLE ---")
        c.execute("PRAGMA table_info(Listings)")
        columns = c.fetchall()
        print(tabulate(columns, headers=["ID", "Name", "Type", "NotNull", "Default", "PK"]))
        
        c.execute("SELECT COUNT(*) FROM Listings")
        print(f"Total listings: {c.fetchone()[0]}")
        
        c.execute("SELECT * FROM Listings LIMIT 3")
        sample_listings = c.fetchall()
        if sample_listings:
            print("\nSample listings:")
            print(tabulate(sample_listings, headers=["ID", "Title", "Location", "Price", "Host"]))
        
        # Show Bookings table info
        print("\n--- BOOKINGS TABLE ---")
        c.execute("PRAGMA table_info(Bookings)")
        columns = c.fetchall()
        print(tabulate(columns, headers=["ID", "Name", "Type", "NotNull", "Default", "PK"]))
        
        c.execute("SELECT COUNT(*) FROM Bookings")
        print(f"Total bookings: {c.fetchone()[0]}")
        
        c.execute("SELECT status, COUNT(*) FROM Bookings GROUP BY status")
        status_counts = c.fetchall()
        if status_counts:
            print("\nBooking status counts:")
            print(tabulate(status_counts, headers=["Status", "Count"]))
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    debug_database()