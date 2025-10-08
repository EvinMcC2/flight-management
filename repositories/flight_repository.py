import sqlite3
from .db_connection import get_connection 

class FlightRepository:

    def get_all_flights(self):

        conn = get_connection()
        if conn is None:
            return []
        
        query = """
        SELECT
            f.id, 
            f.flight_number,
            dep.airport_code AS departure_code, 
            dep.city AS departure_city,
            arr.airport_code AS arrival_code, 
            arr.city AS arrival_city,
            f.departure_time, 
            f.arrival_time, 
            f.status
        FROM Flights f
        JOIN Destinations dep ON f.departure_id = dep.id
        JOIN Destinations arr ON f.arrival_id = arr.id
        ORDER BY f.departure_time ASC;
        """
        
        flights_data = []
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            flights_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during get_all_flights: {e}")
        finally:
            conn.close()
            
        return flights_data

    def add_flight(self, flight_number, departure_id, arrival_id, departure_time, arrival_time, status):
        conn = get_connection()
        if conn is None:
            return None
        
        insert_query = """
        INSERT INTO Flights (flight_number, departure_id, arrival_id, departure_time, arrival_time, status)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(insert_query, (flight_number, departure_id, arrival_id, departure_time, arrival_time, status))
            new_flight_id = cursor.lastrowid
            conn.commit()
            
            return new_flight_id
        except sqlite3.Error as e:
            print(f"Database error during add_flight: {e}")
            return None
        finally:
            conn.close()


    def get_flight_by_number(self, flight_number):
        conn = get_connection()
        if conn is None:
            return []
        
        query = """
        SELECT
            f.id, 
            f.flight_number,
            dep.airport_code AS departure_code, 
            dep.city AS departure_city,
            arr.airport_code AS arrival_code, 
            arr.city AS arrival_city,
            f.departure_time, 
            f.arrival_time, 
            f.status
        FROM Flights f
        JOIN Destinations dep ON f.departure_id = dep.id
        JOIN Destinations arr ON f.arrival_id = arr.id
        WHERE f.flight_number = ?
        ORDER BY f.departure_time ASC;
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (flight_number,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            else:
                return None 
        except sqlite3.Error as e:
            print(f"Database error during get_flight_by_number: {e}")
        finally:
            conn.close()
    

    def get_flights_by_departure_city(self, departureId):
        conn = get_connection()
        if conn is None:
            return []
        
        query = """
        SELECT
            f.id, 
            f.flight_number,
            dep.airport_code AS departure_code, 
            dep.city AS departure_city,
            arr.airport_code AS arrival_code, 
            arr.city AS arrival_city,
            f.departure_time, 
            f.arrival_time, 
            f.status
        FROM Flights f
        JOIN Destinations dep ON f.departure_id = dep.id
        JOIN Destinations arr ON f.arrival_id = arr.id
        WHERE f.departure_id = ?
        ORDER BY f.departure_time ASC;
        """
        
        flights_data = []
        try:
            cursor = conn.cursor()
            cursor.execute(query, (departureId,))
            flights_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during get_flights_by_departure_city: {e}")
        finally:
            conn.close()
            
        return flights_data


    def get_flights_by_departure_time_range(self, start_time, end_time):
        conn = get_connection()
        if conn is None:
            return []
        
        query = """
        SELECT
            f.id, 
            f.flight_number,
            dep.airport_code AS departure_code, 
            dep.city AS departure_city,
            arr.airport_code AS arrival_code, 
            arr.city AS arrival_city,
            f.departure_time, 
            f.arrival_time, 
            f.status
        FROM Flights f
        JOIN Destinations dep ON f.departure_id = dep.id
        JOIN Destinations arr ON f.arrival_id = arr.id
        WHERE f.departure_time BETWEEN ? AND ?
        ORDER BY f.departure_time ASC;
        """
        
        flights_data = []
        try:
            cursor = conn.cursor()
            cursor.execute(query, (start_time, end_time))
            flights_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during get_flights_by_departure_time_range: {e}")
        finally:
            conn.close()
            
        return flights_data


    def update_flight(self, flight_id, flight_number, departure_city, arrival_city, departure_time, arrival_time, status):
        conn = get_connection()
        if conn is None:
            return None
        
        update_query = """
        UPDATE Flights
        SET flight_number = ?, 
            departure_id = (SELECT id FROM Destinations WHERE city = ?),
            arrival_id = (SELECT id FROM Destinations WHERE city = ?),
            departure_time = ?, 
            arrival_time = ?, 
            status = ?
        WHERE id = ?;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(update_query, (flight_number, departure_city, arrival_city, departure_time, arrival_time, status, flight_id))
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error during update_flight: {e}")
            return False
        finally:
            conn.close()