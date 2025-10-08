import sqlite3

DB_NAME = "flight_management.db"

# Destinations data: (airport_code, city, country)
DEFAULT_DESTINATIONS = [
    ('JFK', 'New York', 'USA'),
    ('LAX', 'Los Angeles', 'USA'),
    ('LHR', 'London', 'UK'),
    ('NRT', 'Tokyo', 'Japan'),
    ('SYD', 'Sydney', 'Australia'),
    ('CDG', 'Paris', 'France'),
    ('DXB', 'Dubai', 'UAE'),
    ('AMS', 'Amsterdam', 'Netherlands'),
    ('SIN', 'Singapore', 'Singapore'),
    ('FRA', 'Frankfurt', 'Germany'),
    ('IST', 'Istanbul', 'Turkey'),
    ('HND', 'Tokyo', 'Japan'),
    ('PEK', 'Beijing', 'China'),
    ('MEX', 'Mexico City', 'Mexico'),
    ('SFO', 'San Francisco', 'USA')
]

# Pilots data: (first_name, last_name, license_number)
DEFAULT_PILOTS = [
    ('Alice', 'Johnson', 'PL10001'),
    ('Bob', 'Smith', 'PL10002'),
    ('Charlie', 'Brown', 'PL10003'),
    ('Diana', 'Prince', 'PL10004'),
    ('Edward', 'Kenway', 'PL10005'),
    ('Fiona', 'Gleason', 'PL10006'),
    ('George', 'Lopez', 'PL10007'),
    ('Hannah', 'Arendt', 'PL10008'),
    ('Isaac', 'Newton', 'PL10009'),
    ('Jasmine', 'Lee', 'PL10010'),
    ('Kevin', 'Hart', 'PL10011'),
    ('Laura', 'Palmer', 'PL10012'),
    ('Mike', 'Tyson', 'PL10013'),
    ('Nora', 'Jones', 'PL10014'),
    ('Oscar', 'Wilde', 'PL10015')
]

# Flights data: (flight_number, departure_id, arrival_id, departure_time, arrival_time, status)
DEFAULT_FLIGHTS = [
    ('UA101', 1, 2, '2025-10-15 08:00', '2025-10-15 11:00', 'Scheduled'),
    ('BA202', 3, 1, '2025-10-15 12:30', '2025-10-15 20:00', 'Scheduled'),
    ('JL303', 4, 5, '2025-10-16 01:00', '2025-10-16 10:00', 'Scheduled'),
    ('AF404', 6, 8, '2025-10-16 14:00', '2025-10-16 18:30', 'Scheduled'),
    ('EK505', 7, 9, '2025-10-17 05:00', '2025-10-17 11:00', 'Scheduled'),
    ('AA606', 2, 3, '2025-10-17 19:00', '2025-10-18 01:00', 'Delayed'),
    ('LH707', 10, 6, '2025-10-18 09:00', '2025-10-18 13:00', 'Scheduled'),
    ('QF808', 5, 4, '2025-10-18 22:00', '2025-10-19 06:00', 'Scheduled'),
    ('TK909', 11, 8, '2025-10-19 07:00', '2025-10-19 10:00', 'Scheduled'),
    ('NH110', 12, 13, '2025-10-19 16:00', '2025-10-20 02:00', 'Scheduled'),
    ('AM111', 14, 15, '2025-10-20 10:00', '2025-10-20 13:00', 'Scheduled'),
    ('DL112', 15, 1, '2025-10-20 18:00', '2025-10-21 02:00', 'Scheduled'),
    ('KL113', 8, 3, '2025-10-21 06:00', '2025-10-21 09:00', 'Scheduled'),
    ('SQ114', 9, 7, '2025-10-21 13:00', '2025-10-21 19:00', 'Scheduled'),
    ('CX115', 1, 12, '2025-10-22 00:00', '2025-10-22 10:00', 'Cancelled')
]

# PilotSchedules data: (pilot_id, flight_id, assignment_role)
DEFAULT_PILOT_SCHEDULES = [
    (1, 1, 'Captain'),      
    (2, 1, 'First Officer'),
    (3, 2, 'Captain'),      
    (4, 2, 'First Officer'),
    (5, 3, 'Captain'),      
    (6, 4, 'Captain'),
    (7, 4, 'First Officer'),
    (8, 5, 'Captain'),
    (9, 6, 'First Officer'),
    (10, 7, 'Captain'),
    (11, 7, 'First Officer'),
    (12, 8, 'Captain'),
    (13, 9, 'Captain'),
    (14, 10, 'First Officer'),
    (15, 11, 'Captain')
]

DEFAULT_USERS = [
    ('admin', 'Password1', 'admin', 'administrator@flight.com'),
    ('user', 'Password1', 'user', 'user@flight.com'),
    ('user2', 'user2_hashed_password', 'user', 'user2@flight.com'),
    ('manager', 'Password1', 'manager', 'manager@flight.com')
]

def get_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
    

def initialise_database():
    conn = get_connection()
    if conn is None:
        return
    
    try: 
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Destinations (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           airport_code TEXT NOT NULL UNIQUE,
                           city TEXT NOT NULL,
                           country TEXT NOT NULL
                       );
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Pilots (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL,
                           license_number TEXT NOT NULL UNIQUE,
                           created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                           updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                       );
                       """)


        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Flights (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_number TEXT NOT NULL UNIQUE,
                        departure_id INTEGER NOT NULL,
                        arrival_id INTEGER NOT NULL,
                        departure_time TEXT NOT NULL,
                        arrival_time TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'Scheduled',

                        FOREIGN KEY (departure_id) REFERENCES Destinations(destination_id),
                        FOREIGN KEY (arrival_id) REFERENCES Destinations(destination_id)
                        );
                    """)
        
    
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS PilotSchedules (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            pilot_id INTEGER NOT NULL,
                            flight_id INTEGER NOT NULL,
                            assignment_role TEXT NOT NULL,

                            FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
                            FOREIGN KEY (pilot_id) REFERENCES Pilots(pilot_id),
                            UNIQUE(flight_id, pilot_id)
                        )
                        """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Users (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL UNIQUE,
                           password TEXT NOT NULL,
                           role TEXT NOT NULL,
                           email TEXT,
                           created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                           updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                       );
                       """)

        
        cursor.execute("SELECT COUNT(*) FROM Destinations;")
        if (cursor.fetchone()[0] == 0):
            add_default_data(cursor)
            # without commit the transaction will not be committed and changes will not be carried over when terminal closed
            conn.commit() 

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def add_default_data(cursor):
    cursor.executemany("""
            INSERT OR IGNORE INTO Destinations 
            (airport_code, city, country) 
            VALUES (?, ?, ?)
        """, DEFAULT_DESTINATIONS)
    
    print(f"Seeded {len(DEFAULT_DESTINATIONS)} destinations.")
            
    cursor.executemany("""
        INSERT OR IGNORE INTO Pilots 
        (first_name, last_name, license_number) 
        VALUES (?, ?, ?)
    """, DEFAULT_PILOTS)

    print(f"Seeded {len(DEFAULT_PILOTS)} pilots.")
    
    cursor.executemany("""
        INSERT OR IGNORE INTO Flights 
        (flight_number, departure_id, arrival_id, departure_time, arrival_time, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, DEFAULT_FLIGHTS)

    print(f"Seeded {len(DEFAULT_FLIGHTS)} flights.")

    cursor.executemany("""
        INSERT OR IGNORE INTO PilotSchedules 
        (pilot_id, flight_id, assignment_role) 
        VALUES (?, ?, ?)
    """, DEFAULT_PILOT_SCHEDULES)

    cursor.executemany("""
        INSERT OR IGNORE INTO Users 
        (username, password, role, email) 
        VALUES (?, ?, ?, ?)
    """, DEFAULT_USERS)

    print(f"Seeded {len(DEFAULT_PILOT_SCHEDULES)} pilot schedules.")
