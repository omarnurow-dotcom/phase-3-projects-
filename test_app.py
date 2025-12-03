#!/usr/bin/env python3
"""
Simple tests for House Rental CLI
"""

import sqlite3
import os
from config import DATABASE_NAME

def test_database_exists():
    """Test if database file exists"""
    if os.path.exists(DATABASE_NAME):
        print("✓ Database file exists")
        return True
    else:
        print("✗ Database file not found")
        return False

def test_tables_exist():
    """Test if required tables exist"""
    if not test_database_exists():
        return False
    
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        # Check if Listings table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Listings'")
        if c.fetchone():
            print("✓ Listings table exists")
        else:
            print("✗ Listings table not found")
            return False
        
        # Check if Bookings table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Bookings'")
        if c.fetchone():
            print("✓ Bookings table exists")
        else:
            print("✗ Bookings table not found")
            return False
        
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False

def test_sample_data():
    """Test if sample data exists"""
    if not test_tables_exist():
        return False
    
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        # Check listings count
        c.execute("SELECT COUNT(*) FROM Listings")
        listings_count = c.fetchone()[0]
        print(f"✓ Found {listings_count} listings")
        
        # Check bookings count
        c.execute("SELECT COUNT(*) FROM Bookings")
        bookings_count = c.fetchone()[0]
        print(f"✓ Found {bookings_count} bookings")
        
        conn.close()
        return listings_count > 0 and bookings_count > 0
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("=== House Rental CLI Tests ===")
    
    tests = [
        test_database_exists,
        test_tables_exist,
        test_sample_data
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! The application is ready to use.")
    else:
        print("❌ Some tests failed. Please run 'python database.py' to set up the database.")

if __name__ == "__main__":
    run_tests()