#!/usr/bin/env python3
"""
House Rental CLI Database Setup

This module creates and initializes the SQLite database for the House Rental CLI application.
It creates the necessary tables with proper constraints and populates them with sample data.
"""

import sqlite3
import os
from config import DATABASE_NAME

def create_tables_with_data():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        # Enable foreign key constraints
        c.execute("PRAGMA foreign_keys = ON")

        # Create Listings table with constraints
        c.execute("""
        CREATE TABLE IF NOT EXISTS Listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL CHECK(length(title) > 0),
            location TEXT NOT NULL CHECK(length(location) > 0),
            price_per_day REAL NOT NULL CHECK(price_per_day > 0),
            host_name TEXT NOT NULL CHECK(length(host_name) > 0),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create Bookings table with constraints
        c.execute("""
        CREATE TABLE IF NOT EXISTS Bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL CHECK(length(customer_name) > 0),
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(listing_id) REFERENCES Listings(id) ON DELETE CASCADE,
            CHECK(start_date <= end_date)
        )
        """)

        # Pre-populate Listings with realistic locations in Kenya
        listings = [
            ("Modern Apartment", "Nairobi, Westlands", 80.00, "Alice Mwangi"),
            ("Cozy Villa", "Mombasa, Nyali", 120.00, "John Otieno"),
            ("Beachfront Bungalow", "Diani Beach, Kwale", 150.00, "Mary Wanjiku"),
            ("Urban Studio", "Kisumu, Milimani", 60.00, "Peter Oduor"),
            ("Countryside Cottage", "Naivasha, Lake Naivasha", 70.00, "Grace Njeri"),
            ("Luxury Apartment", "Nairobi, Karen", 200.00, "James Kariuki"),
            ("Seaside Apartment", "Malindi, Bamburi", 100.00, "Susan Karanja"),
            ("Mountain Retreat", "Nairobi, Ngong Hills", 90.00, "David Mutua")
        ]

        # Insert listings if table is empty
        c.execute("SELECT COUNT(*) FROM Listings")
        if c.fetchone()[0] == 0:
            c.executemany("INSERT INTO Listings (title, location, price_per_day, host_name) VALUES (?, ?, ?, ?)", listings)
            print("✓ Sample listings added successfully!")
        else:
            print("✓ Listings table already contains data.")

        # Pre-populate Bookings with some sample bookings
        bookings = [
            (1, "Alice Njeri", "2025-01-05", "2025-01-10", "Approved"),
            (2, "John Mwangi", "2025-01-15", "2025-01-18", "Pending"),
            (3, "Mary Onyango", "2025-01-20", "2025-01-25", "Rejected"),
            (1, "Peter Ochieng", "2025-02-01", "2025-02-03", "Approved"),
            (4, "Grace Wambui", "2025-02-10", "2025-02-15", "Pending")
        ]

        # Insert bookings if table is empty
        c.execute("SELECT COUNT(*) FROM Bookings")
        if c.fetchone()[0] == 0:
            c.executemany("INSERT INTO Bookings (listing_id, customer_name, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)", bookings)
            print("✓ Sample bookings added successfully!")
        else:
            print("✓ Bookings table already contains data.")

        conn.commit()
        print("\n🎉 Database setup completed successfully!")
        print("You can now run 'python main.py' to start the House Rental CLI.")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

def reset_database():
    """Reset the database by deleting and recreating it"""
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print("🗑️  Existing database deleted.")
    create_tables_with_data()

if __name__ == "__main__":
    print("=== House Rental CLI Database Setup ===")
    print("This will create the database with sample data.")
    
    if os.path.exists(DATABASE_NAME):
        choice = input("Database already exists. Reset it? (y/N): ").lower().strip()
        if choice == 'y' or choice == 'yes':
            reset_database()
        else:
            print("Keeping existing database.")
    else:
        create_tables_with_data()
