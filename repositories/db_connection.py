import sqlite3

DB_NAME = "flight_management.db"

def get_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
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
                           destination_id INTEGER PRIMARY KEY,
                           airport_code TEXT NOT NULL UNIQUE,
                           city TEXT NOT NULL,
                           country TEXT NOT NULL
                       );
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Pilots (
                           pilot_id INTEGER PRIMARY KEY,
                           employee_id TEXT NOT NULL UNIQUE, 
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL,
                           license_number TEXT NOT NULL UNIQUE
                       );
                       """)


        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Flights (
                        flight_id INTEGER PRIMARY KEY,
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
        
    
        cursor.exercute("""
                        CREATE TABLE IF NOT EXISTS PilotSchedules (
                            assignment_id INTEGER PRIMARY KEY,
                            pilot_id INTEGER NOT NULL,
                            flight_id INTEGER NOT NULL,
                            assignment_role TEXT NOT NULL,

                            FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
                            FOREIGN KEY (pilot_id) REFERENCES Pilots(pilot_id),
                            UNIQUE(flight_id, pilot_id)
                        )
                        """)
        
        cursor.execute("SELECT COUNT(*) FROM Destinations;")
        if (cursor.fetchone()[0] == 0):
            _seed_destinations(cursor)

            conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def _seed_destinations(cursor):
    destinations = [
        (1, 'New York', 'USA'),
        (2, 'Los Angeles', 'USA'),
        (3, 'London', 'UK'),
        (4, 'Tokyo', 'Japan'),
        (5, 'Sydney', 'Australia')
    ]
    cursor.executemany("INSERT INTO Destinations (destination_id, city, country) VALUES (?, ?, ?);", destinations)

  # will change to use txt files (less cluttered)
    