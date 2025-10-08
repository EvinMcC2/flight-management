from repositories.pilot_repository import PilotRepository
from repositories.pilot_schedule_repository import PilotScheduleRepository

class PilotService:
    def __init__(self):
        self.repository = PilotRepository()
        self.schedule_repository = PilotScheduleRepository()

    def get_all_pilots(self):
        pilots_data = self.repository.get_all_pilots()

        if not pilots_data:
            return "No pilots found in the system."
        
        return pilots_data
    
    def add_pilot(self, first_name, last_name, license_number):
        if self.get_pilot_by_license(license_number):
            print(f"Error: A pilot with license number '{license_number}' already exists. License numbers must be unique.")
            return False

        return self.repository.add_pilot(first_name, last_name, license_number)
    
    def get_pilot_by_id(self, pilot_id):
        pilot_data = self.repository.get_pilot_by_id(pilot_id)
        
        if not pilot_data:
            print(f"No pilots found with ID: {pilot_id}")
            return None
    
        return pilot_data
    
    def get_pilot_by_license(self, license):
        pilot_data = self.repository.get_pilot_by_license(license)
        
        if not pilot_data:
            print(f"No pilots found with license: {license}")
            return None
    
        return pilot_data
    
    def update_pilot(self, pilot_id, first_name, last_name, license_number):

        if not self.repository.get_pilot_by_id(pilot_id):
            print(f"Error: Cannot update. Pilot with ID {pilot_id} does not exist.")
            return False

        existing_pilot_by_license = self.get_pilot_by_license(license_number)
        if existing_pilot_by_license and existing_pilot_by_license['id'] != pilot_id:
            print(f"Error: License number '{license_number}' is already assigned to another pilot (ID: {existing_pilot_by_license['id']}). Cannot update.")
            return False

        success = self.repository.update_pilot(pilot_id, first_name, last_name, license_number)
        if success:
            return self.repository.get_pilot_by_id(pilot_id)
        else:
            print("Update failed due to a database error.")
            return None
        
    def get_pilot_schedule(self, pilot_id):
        schedule_data = self.schedule_repository.get_schedule_by_pilot_id(pilot_id)
    
        return schedule_data 
    
    def get_all_schedules(self):
        schedule_data = self.schedule_repository.get_all_pilots_schedule()
        return schedule_data

    def schedule_pilot_for_flight(self, pilot_id: int, flight_id: int, role: str) -> bool:
        schedule_id = self.schedule_repository.add_pilot_schedule(pilot_id, flight_id, role)
        
        return schedule_id is not None