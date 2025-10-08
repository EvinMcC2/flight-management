from datetime import datetime
from getpass import getpass
from repositories.db_connection import initialise_database
from services.flight_service import FlightService
from services.destination_service import DestinationService
import pandas as pd

from services.pilot_service import PilotService
from services.user_service import UserService

# PEP 8 Standard Python style mandates snake_case for variable names

# use login details 
# username: admin
# password: Password1

CURRENT_USER_ROLE = None
VALID_ROLES = ['admin', 'manager', 'user']
running = True
datetime_format = '%Y-%m-%d %H:%M'
pilot_management_permission = True

MENU_MAP = {
    '1': ('View All Flights', ['admin', 'manager', 'user']),
    '2': ('Search for a Flight', ['admin', 'manager', 'user']),
    '3': ('Add a New Flight', ['admin', 'manager']),
    '4': ('Update Flight Information', ['admin', 'manager']),
    '5': ('Manage Pilots', ['admin', 'manager']),
    '6': ('View/Update Destinations', ['admin', 'manager']),
    '7': ('Delete a Flight', ['admin']),
    '8': ('Delete flights that have been cancelled', ['admin']),
    '9': ('Delete flights that have already departed', ['admin']),
    '10': ('Delete all flights without a pilot assigned', ['admin']),
    '11': ('Exit Application', ['admin', 'manager', 'user']),
}


# o	Add a New Flight
# o	View Flights by Criteria
# o	Update Flight Information
# o	Assign Pilot to Flight
# o	View Pilot Schedule
# o	View/Update Destination Information

# def display_menu():
#   print("\n--- Flight Management System ---")
#   print("1. View All Flights")
#   print("2. Search for a Flight")
#   print("3. Add a New Flight") # TODO() this must also allow assigning a pilot to the flight
#   print("4. Update Flight Information")
#   print("5. Manage Pilots")
#   print("6. View/Update Destinations")
#   print("7. Delete a Flight") # this must also delete any pilot assignments for that flight
#   print("8. Delete flights that have been cencelled") # this must also delete any pilot assignments for that flight
#   print("9. Delete flights that have already departed") # this must also delete any pilot assignments for that flight
#   print("10. Delete all flights without a pilot assigned")
#   print("11. Exit Application")
#   try:
#       choice = input("Enter your choice (1-7): ")
#       return choice.strip()
#   except Exception:
#       return None

def display_menu(role):

    print(f"\n--- Flight Management System ({role.upper()}) ---")
    
    # We use a list to store only the valid menu numbers for this role
    available_choices = []

    for choice_num, (description, allowed_roles) in MENU_MAP.items():
        if role in allowed_roles:
            print(f"{choice_num}. {description}")
            available_choices.append(choice_num)
            
    try:
        choice = input(f"Enter your choice ({available_choices[0]}-{available_choices[-1]}): ")
        if choice in available_choices:
            return choice.strip()
        else:
            print(f"\nInvalid choice for role '{role}'. Please try again.")
            return None
    except Exception:
        return None


def check_permission(choice_num):
    """Checks if the CURRENT_USER_ROLE has permission for a specific choice number."""
    global CURRENT_USER_ROLE
    
    # Check if the choice number exists in the map
    if choice_num in MENU_MAP:
        # Get the allowed roles for this choice
        allowed_roles = MENU_MAP[choice_num][1]
        
        if CURRENT_USER_ROLE in allowed_roles:
            return True
        else:
            print(f"\n--- PERMISSION DENIED ---")
            print(f"Your role ({CURRENT_USER_ROLE}) does not have permission for this action.")
            print(f"Allowed roles: {', '.join(allowed_roles)}")
            print(f"-------------------------\n")
            return False
    # If the choice is not in the map, it's either Exit or an invalid choice, handled elsewhere
    return True


def initial_login_prompt(user_service):
    print("Welcome to the Flight Management System.")
    print("Available demonstration roles: admin, manager, user")
    
    while True:
        username = input("Enter your username to continue: ").strip()
        password = getpass("Enter your password to continue: ").strip()
        role = user_service.user_login(username, password)
        if not role:
            print("\nLogin failed. Please try again.\n")
            continue

        if role in VALID_ROLES:
            print(f"\nLogin successful. Your role is: {role}\n")
            return role
        else:
            print("Login failed. Invalid role.")
  

def get_valid_integer_input(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a whole number (ID).")


def get_valid_destination_id_input(prompt, dest_service):
    while True:
        destination_id = get_valid_integer_input(prompt)
        
        if dest_service.is_valid_id(destination_id):
            return destination_id
        else:
            print(f"Error: Destination ID '{destination_id}' is invalid or does not exist.")
            print("\nAvailable Destinations:")
            print(dest_service.get_all_destinations())


def get_valid_city_input(prompt, dest_service, allowNull = False):
    while True:
        print("\nAvailable Cities:")
        print(dest_service.get_all_destinations())
        city = input(prompt).strip()
        
        if allowNull and city == "":
            return None
        
        if dest_service.is_valid_city(city):
            return city
        else:
            print("\nPlease enter a valid city name.\n")
            

def get_valid_datetime_input(prompt, datetime_format='%Y-%m-%d %H:%M', allowNull = False):
    """Continuously prompts the user until a valid datetime string is entered."""
    while True:
        date_str = input(prompt).strip()
        if allowNull and date_str == "":
            return None
        try:
            datetime.strptime(date_str, datetime_format)
            return date_str
        except ValueError:
            print(f"Invalid date/time format. Please use the required format: {datetime_format}")


def get_valid_pilot_id_input(prompt, pilot_service):
    while True:
        pilot_id = get_valid_integer_input(prompt)
        if pilot_service.get_pilot_by_id(pilot_id):
            return pilot_id
        else:
            print(f"Error: Pilot ID '{pilot_id}' is invalid or does not exist.")
            print("\nAvailable Pilots:")
            print(pilot_service.get_all_pilots())


def display_flights_table(flights_data): # TODO - use this function below
    if not flights_data:
        print("No flights found.")
        return
    
    df = pd.DataFrame(flights_data)
    df.columns = [
        'ID', 'Flight Number', 'Dep. Code', 'Dep. City', 'Arr. Code', 
        'Arr. City', 'Departure Time', 'Arrival Time', 'Status'
    ]
    print(df.to_string(index=False))


def pilotMenu():
    print("\n--- Pilot Management ---")
    print("1. View All Pilots")
    print("2. Add a New Pilot")
    print("3. Update Pilot Information")
    print("4. View Pilot Schedule (Placeholder)")
    print("5. Return to Main Menu")
    try:
        choice = input("Enter your choice (1-5): ")
        return choice.strip()
    except Exception:
        return None
    

def pilot_management_loop(pilot_service):
    while True:
        pilot_choice = pilotMenu()

        if pilot_choice == '1':
            pilots = pilot_service.get_all_pilots()
            print("\nAll Pilots")
            print(f"{pilots}\n")
            
        elif pilot_choice == '2':
            print("\nAdd New Pilot")
            first_name = input("Enter pilot first name: ").strip()
            last_name = input("Enter pilot last name: ").strip()
            license_number = input("Enter pilot license number: ").strip()

            if not (first_name and last_name and license_number):
                print("Error: All fields are required.")
                continue
                
            result = pilot_service.add_pilot(first_name, last_name, license_number)
            if result:
                print(f"\nPilot {first_name} {last_name} added successfully.\n")
            else:
                print("\nFailed to add new pilot.\n")
                
        elif pilot_choice == '3':
            print("\nUpdate Pilot Information")
            
            print("\nCurrent Pilots:")
            print(pilot_service.get_all_pilots())
            pilot_id = get_valid_pilot_id_input("Enter the ID of the pilot to update: ", pilot_service)
            
            existing_pilot = pilot_service.get_pilot_by_id(pilot_id)

            print("\nLeave fields empty to keep current value")
            new_first_name = input(f"Update first name ({existing_pilot['first_name']}): ").strip() or existing_pilot['first_name']
            new_last_name = input(f"Update last name ({existing_pilot['last_name']}): ").strip() or existing_pilot['last_name']
            new_license_number = input(f"Update license number ({existing_pilot['license_number']}): ").strip() or existing_pilot['license_number']

            updated_pilot = pilot_service.update_pilot(
                pilot_id, new_first_name, new_last_name, new_license_number
            )

            if updated_pilot:
                print(f"\nPilot ID {pilot_id} updated successfully.")
                
                df = pd.DataFrame([updated_pilot])
                df.columns = ['ID', 'First Name', 'Last Name', 'License Number']
                print(df.to_string(index=False) + "\n")
            else:
                print("\nFailed to update pilot information. Check console for details.\n")
            
        elif pilot_choice == '4':
            print("\nAction: View Pilot Schedule. (Functionality to be implemented when flight assignment is added).\n")
            # need to create flight assignment respository and service 

        elif pilot_choice == '5':
            print("Returning to Main Menu.")
            break
        
        elif pilot_choice is not None:
            print("Invalid choice. Please enter a number from 1 to 5.")


initialise_database()
flight_service = FlightService()
user_service = UserService()
destination_service = DestinationService()
pilot_service = PilotService()
print("Flight Service initialized successfully.")

CURRENT_USER_ROLE = initial_login_prompt(user_service)

while running:
    choice = display_menu(CURRENT_USER_ROLE)

    if choice == '1':
        print("\nAction: Viewing All Flights...")
        output_table = flight_service.get_all_flights()
        print(output_table)
        
    elif choice == '2':
        # provide options for searching flights
        # offer different search criteria
        # e.g., by flight number, by departure/arrival location, by date range,
        search_criteria = input("Enter search criteria number (1: flight number, 2: departure city, 3: departure time range): ")
        print(f"Searching for flights matching: {search_criteria} (Functionality to be implemented)")
        flight_data = None
        if search_criteria.strip() == "1":
            flight_number = input("Enter the flight number to search: ").strip()
            flight_data = flight_service.get_flight_by_number(flight_number)
        elif search_criteria.strip() == "2":
            print("Available Destinations:")
            print(destination_service.get_all_destinations())
            departure_id = get_valid_destination_id_input("Enter the departure location ID: ", destination_service)

            flight_data = flight_service.get_flights_by_departure_city(departure_id)
        elif search_criteria.strip() == "3":
            departure_time_start = get_valid_datetime_input(
            f"Enter the start departure time for range ({datetime_format}): ", 
            datetime_format
            )
            departure_time_end = get_valid_datetime_input(
            f"Enter the end departure time for range ({datetime_format}): ", 
            datetime_format
            )
            flight_data = flight_service.get_flights_by_departure_time_range(departure_time_start, departure_time_end)
        else:
            print("No search criteria provided.")
            continue

        if flight_data:
            print(f"\n{flight_data}\n")
        else:
            print("\n ---- No flights found matching the criteria. ---- \n")

    elif choice == '3':
        flight_number = input("Enter flight number: ")
        print("Available Destinations:")
        print(destination_service.get_all_destinations())

        departure_id = get_valid_destination_id_input("Enter the departure location ID: ", destination_service)
    
        arrival_id = get_valid_destination_id_input("Enter the arrival location ID: ", destination_service)
        
        departure_time = get_valid_datetime_input(
        f"Enter the departure time ({datetime_format}): ", 
        datetime_format
        )
        arrival_time = get_valid_datetime_input(
        f"Enter the arrival time ({datetime_format}): ", 
        datetime_format
        )
        status = input("Enter the flight status ( Scheduled, Delayed, Cancelled): ")
    
        result = flight_service.add_new_flight(
            flight_number, departure_id, arrival_id, departure_time, arrival_time, status)
        
        if result:
            print("\nNew flight added successfully.\n")
        else:
            print("\nFailed to add new flight.\n")
    
    # print flights either result
        output_table = flight_service.get_all_flights()
        print(output_table)

    elif choice == '4':
        # update flight information
        # e.g., change status, reschedule times, etc.
        # could reuse some of the input validation from adding a new flight
        print("\nAction: Viewing All Flights...")
        output_table = flight_service.get_all_flights()
        print(f"\n{output_table}\n")
        flight_number = input("Enter the flight number to search: ").strip()
        flight_data = flight_service.get_flight_by_number(flight_number)

        if not flight_data:
            print(f"No flights found with flight: {flight_number}")
            continue

        df = pd.DataFrame([flight_data])
        df.columns = [
            'ID', 'Flight Number', 'Dep. Code', 'Dep. City', 'Arr. Code', 
            'Arr. City', 'Departure Time', 'Arrival Time', 'Status'
        ]
        print("Current flight details:")
        print(f"\n{df.to_string(index=False)}\n")

        flight_number = input(f"Update flight number {flight_data["flight_number"]} or leave empty and enter: ")
        if not flight_number:
            flight_number = flight_data["flight_number"]

        # it seem illogical to force users to enter a destination id sometimes and a city other times - this should be consistent but this is to show we can do both. (ideally they would be provided with dropdown to easily select from)
        flight_departure_city = get_valid_city_input(f"Update departure city ${flight_data["departure_city"]} or leave empty and enter: ", destination_service, True)
        if not flight_departure_city:
            flight_departure_city = flight_data["departure_city"]

        flight_arrival_city = get_valid_city_input(f"Update arrival city ${flight_data["arrival_city"]} or leave empty and enter: ", destination_service, True)
        if not flight_arrival_city:
            flight_arrival_city = flight_data["arrival_city"]

        flight_departure_time = get_valid_datetime_input(
            f"Update departure time ({flight_data["departure_time"]}) or leave empty and enter: ", 
            datetime_format, True
        )
        if not flight_departure_time:
            flight_departure_time = flight_data["departure_time"]

        flight_arrival_time = get_valid_datetime_input(
            f"Update arrival time ({flight_data["arrival_time"]}) or leave empty and enter: ", 
            datetime_format, True
        )
        if not flight_arrival_time:
            flight_arrival_time = flight_data["arrival_time"]

        flight_status = input(f"Update flight status ({flight_data["status"]}) or leave empty and enter: ")
        if not flight_status:
            flight_status = flight_data["status"]
        
        flight_data = flight_service.update_flight_information(
            flight_data["id"], flight_number, flight_departure_city, flight_arrival_city, 
            flight_departure_time, flight_arrival_time, flight_status
        )
        if not flight_data:
            print(f"Flight data failed to update: {flight_number}")
            continue

        df = pd.DataFrame([flight_data])
        df.columns = [
            'ID', 'Flight Number', 'Dep. Code', 'Dep. City', 'Arr. Code', 
            'Arr. City', 'Departure Time', 'Arrival Time', 'Status'
        ]
        print("Current flight details:")
        print(f"\n{df.to_string(index=False)}\n")

    elif choice == '5':
        pilot_management_loop(pilot_service)

    elif choice == '6':

        print("View/Update Destinations - Functionality to be implemented")
        # view/update destinations
        # e.g., add new destination, update existing destination info, etc.
        
    elif choice == '7':
        print("\nExiting application. Goodbye!\n")
        running = False
        
    else:
        print("Invalid or unimplemented choice. Please try again.")