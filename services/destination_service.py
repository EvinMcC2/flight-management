import pandas as pd
from repositories.destination_repository import DestinationRepository

class DestinationService:
    def __init__(self):
        self.repository = DestinationRepository()

    def is_valid_id(self, destination_id):

        if not isinstance(destination_id, int) or destination_id <= 0:
            return False

        return self.repository.is_valid_id(destination_id)
    
    def is_valid_city(self, city):
        if not isinstance(city, str) or not city.strip():
            return False
        
        return self.repository.is_valid_city(city)
    

    def get_all_destinations(self):
        destinations_data = self.repository.get_all_destinations()

        if not destinations_data:
            return "No destinations found in the system."
        
        df = pd.DataFrame(destinations_data)

        return df.to_string(index=False)