from db_connection import get_connection
import sqlite3

# TODO() expand 
class PilotScheduleRepository:
    
    def get_schedule_by_pilot_id(self, pilot_id):
        conn = get_connection()
        if conn is None:
            return []
            
        query = """
        SELECT
            F.flight_number,
            D_DEP.city AS departure_city,
            D_ARR.city AS arrival_city,
            PS.assignment_role,
            F.departure_time,
            F.arrival_time,
            F.status
        FROM
            PilotSchedules PS
        JOIN
            Flights F ON PS.flight_id = F.id
        JOIN
            Destinations D_DEP ON F.departure_id = D_DEP.id
        JOIN
            Destinations D_ARR ON F.arrival_id = D_ARR.id
        WHERE
            PS.pilot_id = ?
        ORDER BY
            F.departure_time;
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, (pilot_id,))
            
            schedule_data = [dict(row) for row in cursor.fetchall()]
            return schedule_data
            
        except sqlite3.Error as e:
            print(f"Error fetching pilot schedule for ID {pilot_id}: {e}")
            return []
        finally:
            conn.close()