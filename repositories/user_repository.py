from .db_connection import get_connection
import sqlite3

class UserRepository:

    def authenticate_user(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                return user
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            conn.close()

    def get_all_users(self):
        conn = get_connection()
        if conn is None:
            return []
        
        query = "SELECT id, username, role, email, created_at, updated_at FROM Users;"
    
        user_data = []
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            user_data = [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during get_all_users: {e}")
        finally:
            conn.close()
            
        return user_data