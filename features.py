#!/usr/bin/env python3
"""
Additional features for House Rental CLI
"""

import sqlite3
from tabulate import tabulate
from datetime import datetime, timedelta
from config import DATABASE_NAME, CURRENCY_SYMBOL, TABLE_FORMAT

def search_listings():
    """Search listings by location or price range"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    print("1. Search by location")
    print("2. Search by price range")
    choice = input("Choose search type: ").strip()
    
    if choice == "1":
        location = input("Enter location to search: ").strip()
        c.execute("SELECT * FROM Listings WHERE location LIKE ?", (f"%{location}%",))
    elif choice == "2":
        min_price = float(input("Minimum price: "))
        max_price = float(input("Maximum price: "))
        c.execute("SELECT * FROM Listings WHERE price_per_day BETWEEN ? AND ?", (min_price, max_price))
    
    rows = c.fetchall()
    if rows:
        formatted_rows = [[r[0], r[1], r[2], f"{CURRENCY_SYMBOL}{r[3]:.2f}", r[4]] for r in rows]
        print(tabulate(formatted_rows, headers=["ID", "Title", "Location", "Price/day", "Host"], tablefmt=TABLE_FORMAT))
    else:
        print("No listings found.")
    conn.close()

def view_availability():
    """Check availability for specific dates"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    start_date = input("Check availability from (YYYY-MM-DD): ")
    end_date = input("To (YYYY-MM-DD): ")
    
    c.execute("""
        SELECT L.id, L.title, L.location, L.price_per_day 
        FROM Listings L 
        WHERE L.id NOT IN (
            SELECT DISTINCT B.listing_id FROM Bookings B 
            WHERE B.status = 'Approved' 
            AND ((B.start_date <= ? AND B.end_date >= ?) OR (B.start_date <= ? AND B.end_date >= ?))
        )
    """, (start_date, start_date, end_date, end_date))
    
    rows = c.fetchall()
    if rows:
        formatted_rows = [[r[0], r[1], r[2], f"{CURRENCY_SYMBOL}{r[3]:.2f}"] for r in rows]
        print(tabulate(formatted_rows, headers=["ID", "Title", "Location", "Price/day"], tablefmt=TABLE_FORMAT))
    else:
        print("No available listings for these dates.")
    conn.close()

def cancel_booking():
    """Cancel a pending booking"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    c.execute("SELECT * FROM Bookings WHERE status = 'Pending'")
    bookings = c.fetchall()
    if not bookings:
        print("No pending bookings to cancel.")
        return
    
    print(tabulate(bookings, headers=["ID", "Listing", "Customer", "Start", "End", "Status"]))
    booking_id = int(input("Enter booking ID to cancel: "))
    
    c.execute("DELETE FROM Bookings WHERE id = ? AND status = 'Pending'", (booking_id,))
    if c.rowcount > 0:
        print("Booking cancelled successfully!")
    else:
        print("Booking not found or cannot be cancelled.")
    
    conn.commit()
    conn.close()