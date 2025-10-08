import pandas as pd
# Import the repository to handle data access
from repositories.flight_repository import FlightRepository 
from models.entities import Flight 

class FlightService:
    def __init__(self):
        self.repository = FlightRepository()

    def get_all_flights(self):
        flights_data = self.repository.get_all_flights()

        if not flights_data:
            return "No flights found in the system."
    
        df = pd.DataFrame(flights_data)
        df.columns = [
            'ID', 'Flight Number', 'Dep. Code', 'Dep. City', 'Arr. Code', 
            'Arr. City', 'Departure Time', 'Arrival Time', 'Status'
        ]

        # Setting index=False removes the default row numbers
        return df.to_string(index=False)
    
    def add_new_flight(self, flight_number, departure_id, arrival_id, departure_time, arrival_time, status):
        completed = self.repository.add_flight(
            flight_number, departure_id, arrival_id, departure_time, arrival_time, status)
        return completed
    
    def get_flight_by_number(self, flight_number):
        flight_data = self.repository.get_flight_by_number(flight_number)
        
        if not flight_data:
            print(f"No flights found with flight number: {flight_number}")
            return None
    
        return flight_data
    

    def get_flights_by_departure_city(self, departureId):
        flights_data = self.repository.get_flights_by_departure_city(departureId)
        
        if not flights_data:
            print(f"No flights found departing from city: {departureId}")
            return
        
        df = pd.DataFrame(flights_data)
        df.columns = [
            'ID', 'Flight Number', 'Dep. Code', 'Dep. City', 'Arr. Code', 
            'Arr. City', 'Departure Time', 'Arrival Time', 'Status'
        ]
        
        return df.to_string(index=False)


    def get_flights_by_departure_time_range(self, start_time, end_time):
        flights_data = self.repository.get_flights_by_departure_time_range(start_time, end_time)
        
        if not flights_data:
            print(f"No flights found departing between {start_time} and {end_time}.")
            return
        
        df = pd.DataFrame(flights_data)
        df.columns = [
            'ID', 'Flight Number', 'Dep. Code', 'Dep. City', 'Arr. Code', 
            'Arr. City', 'Departure Time', 'Arrival Time', 'Status'
        ]
        
        return df.to_string(index=False)
    
    def update_flight_information(self, flight_id, flight_number, departure_city, arrival_city, departure_time, arrival_time, status):
        completed = self.repository.update_flight(
            flight_id, flight_number, departure_city, arrival_city, departure_time, arrival_time, status)
        
        if completed:
            return self.repository.get_flight_by_number(flight_number)
        else: 
            print(f"Failed to update flight with Flight Number: {flight_number}")
            return None