from repositories.db_connection import initialise_database

running = True



# o	Add a New Flight
# o	View Flights by Criteria
# o	Update Flight Information
# o	Assign Pilot to Flight
# o	View Pilot Schedule
# o	View/Update Destination Information

def main_menu():
  print("\n--- Flight Management System ---")
  print("1. View All Flights")
  print("2. Search for a Flight")
  print("2. Add a New Flight")
  print("2. Update Flight Information")
  print("3. Manage Pilots")
  print("2. View/Update Destinations")
  print("4. Exit Application")

  choice = int(input("Enter your choice: "))
  if choice == '1':
    print("View All Flights")
  elif choice == '2':
    print("Search for a Flight")
  elif choice == '3':
    print("Manage Pilots")


while running:
  initialise_database()
  running = main_menu()