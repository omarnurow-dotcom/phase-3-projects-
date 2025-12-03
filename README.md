# House Rental CLI

Project Name: House Rental CLI
Description: A command-line application to manage house and apartment rentals. Hosts can add listings, manage bookings, approve or reject reservations, and view earnings reports. Data is stored locally using SQLite.

# Features

Add House/Apartment Listings
Hosts can create rental listings with title, location, price per day, and host name.

View All Listings
Displays all available listings in a neat table format.

Create Bookings
Customers can book a listing specifying start and end dates. Bookings are initially Pending.

Approve or Reject Bookings
Hosts can approve or reject pending bookings.

Earnings Report
Displays total earnings per listing based on approved bookings.

## Database Tables
Listings Table
Column Name	Type	Description
id	INTEGER PK	Unique house ID
title	TEXT	House or apartment name
location	TEXT	Address or city
price_per_day	REAL	Rental price per day
host_name	TEXT	Owner of the property
Bookings Table
Column Name	Type	Description
id	INTEGER PK	Unique booking ID
listing_id	INTEGER FK	Linked to Listings.id
customer_name	TEXT	Name of the renter
start_date	TEXT	Booking start date
end_date	TEXT	Booking end date
status	TEXT	Pending / Approved / Rejected
## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd house_rental_cli
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or on Windows:
   # venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python database.py
   ```

5. **Test the setup (optional):**
   ```bash
   python test_app.py
   ```

## Usage

Run the CLI application:
```bash
python main.py
```


You will see a menu like this:

--- House Rental CLI ---
1. Add Listing
2. View All Listings
3. Create Booking
4. Approve/Reject Booking
5. View Earnings Report
6. Exit


Select an option by entering its number.
Follow the prompts to add listings, create bookings, manage bookings, and view earnings.

## Sample Data

The database comes pre-populated with realistic listings in Kenya:

- **Nairobi, Westlands** - Modern Apartment ($80/day)
- **Mombasa, Nyali** - Cozy Villa ($120/day)
- **Diani Beach, Kwale** - Beachfront Bungalow ($150/day)
- **Kisumu, Milimani** - Urban Studio ($60/day)
- **Naivasha, Lake Naivasha** - Countryside Cottage ($70/day)
- **Nairobi, Karen** - Luxury Apartment ($200/day)
- **Malindi, Bamburi** - Seaside Apartment ($100/day)
- **Nairobi, Ngong Hills** - Mountain Retreat ($90/day)

Sample bookings with different statuses: **Pending**, **Approved**, **Rejected**.

## Key Improvements Made

- **Input Validation**: All user inputs are now validated for correct format and constraints
- **Error Handling**: Comprehensive error handling for database operations and user input
- **Date Validation**: Proper date format validation and logical date checking
- **Booking Conflicts**: Prevention of double-bookings for the same dates
- **Database Constraints**: Added proper database constraints and foreign key relationships
- **Configuration Management**: Centralized configuration in `config.py`
- **Better Formatting**: Improved table formatting and currency display
- **Testing**: Added basic test functionality to verify setup
- **Documentation**: Enhanced code documentation and user guidance

## File Structure

```
house_rental_cli/
├── main.py           # Main CLI application
├── database.py       # Database setup and initialization
├── config.py         # Configuration settings
├── test_app.py       # Basic tests
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── house_rental.db   # SQLite database (created after setup)
```

## Technologies Used

- **Python 3**: Core programming language
- **SQLite**: Local database storage (via sqlite3)
- **Tabulate**: Table formatting in CLI
- **Datetime**: Date validation and manipulation

## Troubleshooting

- **Database not found error**: Run `python database.py` to create the database
- **Import errors**: Make sure you've installed dependencies with `pip install -r requirements.txt`
- **Permission errors**: Ensure you have write permissions in the project directory
- **Date format errors**: Use YYYY-MM-DD format for all dates

## License

This project is open-source and free to use.