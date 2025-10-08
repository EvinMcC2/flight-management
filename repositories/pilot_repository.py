import sqlite3
from .db_connection import get_connection

class PilotRepository:

    def get_all_pilots(self):
        conn = get_connection()
        if conn is None:
            return []
        
        query = "SELECT id, first_name, last_name, license_number FROM Pilots;"
    
        pilot_data = []
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            pilot_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during get_all_pilots: {e}")
        finally:
            conn.close()
            
        return pilot_data
    
    def add_pilot(self, first_name, last_name, license_number):
        conn = get_connection()
        if conn is None:
            return False
        
        insert_query = """
        INSERT INTO Pilots (first_name, last_name, license_number)
        VALUES (?, ?, ?);
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(insert_query, (first_name, last_name, license_number))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error during add_pilot: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_pilot_by_id(self, pilot_id):
        conn = get_connection()
        if conn is None:
            return None
        
        query = "SELECT id, first_name, last_name, license_number FROM Pilots WHERE id = ?;"
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (pilot_id,))
            pilot = cursor.fetchone()
            if pilot:
                return dict(pilot)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error during get_pilot_by_id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_pilot_by_license(self, license_number):
        conn = get_connection()
        if conn is None:
            return None
        
        query = "SELECT id, first_name, last_name, license_number FROM Pilots WHERE license_number = ?;"
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (license_number,))
            pilot = cursor.fetchone()
            if pilot:
                return dict(pilot)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error during get_pilot_by_license: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def update_pilot(self, pilot_id, first_name, last_name, license_number):
        """Updates the information for an existing pilot."""
        conn = get_connection()
        if conn is None: return False
        
        query = """
        UPDATE Pilots 
        SET first_name = ?, last_name = ?, license_number = ?
        WHERE id = ?;
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query, (first_name, last_name, license_number, pilot_id))
            conn.commit()
            # Check if one row was successfully updated
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error during update_pilot: {e}")
            return False
        finally:
            conn.close()