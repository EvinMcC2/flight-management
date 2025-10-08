from .db_connection import get_connection 
import sqlite3

class DestinationRepository:

    def is_valid_id(self, destination_id):
        conn = get_connection()
        if conn is None:
            print("ERROR: Database connection failed during ID validation.")
            return False
            
        query = "SELECT COUNT(*) FROM Destinations WHERE id = ?"
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (destination_id,))
            count = cursor.fetchone()[0]
            return count == 1
            
        except sqlite3.Error as e:
            print(f"Database error during ID check: {e}")
            return False
        finally:
            conn.close()

    def is_valid_city(self, city):
        conn = get_connection()
        if conn is None:
            print("ERROR: Database connection failed during city validation.")
            return False
            
        query = "SELECT COUNT(*) FROM Destinations WHERE city = ?"
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (city,))
            count = cursor.fetchone()[0]
            return count > 0
            
        except sqlite3.Error as e:
            print(f"Database error during city check: {e}")
            return False
        finally:
            conn.close()

    def get_all_destinations(self):
        conn = get_connection()
        if conn is None:
            return []
        
        query = "SELECT id, airport_code, city, country FROM Destinations;"
    
        destination_data = []
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            destination_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during get_all_flights: {e}")
        finally:
            conn.close()
            
        return destination_data