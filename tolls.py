import csv
from datetime import datetime


VEHICLE_FILE = 'vehicles.csv'
ACCESS_LOG_FILE = 'toll_log.csv'


TOLL_RATES = {
    "Car": 10,  
    "Truck": 20,
    "Motorcycle": 5
}

def add_vehicle():
    
    vehicle_id = input("Enter the vehicle ID (e.g., ABC123): ")
    vehicle_type = input("Enter the vehicle type (Car, Truck, Motorcycle): ").capitalize()
    owner_name = input("Enter the owner's name: ")
    contact_number = input("Enter the contact number: ")

    with open(VEHICLE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([vehicle_id, vehicle_type, owner_name, contact_number])
    print(f"Vehicle '{vehicle_id}' registered successfully.")

def view_vehicles():
    
    try:
        with open(VEHICLE_FILE, mode='r') as file:
            reader = csv.reader(file)
            print("\n{:<15} {:<15} {:<25} {:<15}".format('Vehicle ID', 'Type', 'Owner Name', 'Contact'))
            print("=" * 70)
            for row in reader:
                print("{:<15} {:<15} {:<25} {:<15}".format(row[0], row[1], row[2], row[3]))
            print("=" * 70)
    except FileNotFoundError:
        print("Vehicle file not found. Please register vehicles first.")

def calculate_toll(vehicle_type, distance):
    
    if vehicle_type in TOLL_RATES:
        return TOLL_RATES[vehicle_type] * distance
    else:
        print("Invalid vehicle type.")
        return 0

def log_toll_entry(vehicle_id):
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ACCESS_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([vehicle_id, 'Entry', timestamp])
    print(f"Vehicle '{vehicle_id}' has entered the toll gate.")

def log_toll_exit(vehicle_id, vehicle_type, distance):
    
    toll_fee = calculate_toll(vehicle_type, distance)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ACCESS_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([vehicle_id, 'Exit', timestamp, toll_fee])
    print(f"Vehicle '{vehicle_id}' has exited the toll gate. Toll fee: ₹{toll_fee:.2f}")

def view_toll_logs():
    
    try:
        with open(ACCESS_LOG_FILE, mode='r') as file:
            reader = csv.reader(file)
            print("\n{:<15} {:<15} {:<20} {:<10}".format('Vehicle ID', 'Action', 'Timestamp', 'Toll Fee'))
            print("=" * 70)
            for row in reader:
                print("{:<15} {:<15} {:<20} {:<10}".format(row[0], row[1], row[2], row[3] if len(row) > 3 else "N/A"))
            print("=" * 70)
    except FileNotFoundError:
        print("Toll log file not found.")

def generate_daily_report():
    
    total_toll = 0
    try:
        with open(ACCESS_LOG_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == 'Exit' and len(row) > 3:
                    total_toll += float(row[3])
        print(f"Total toll collected today: ₹{total_toll:.2f}")
    except FileNotFoundError:
        print("Toll log file not found.")

def delete_vehicle():
    
    vehicle_id = input("Enter the Vehicle ID to delete: ")
    vehicles = []
    found = False

    try:
        with open(VEHICLE_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != vehicle_id:
                    vehicles.append(row)
                else:
                    found = True
    
        if found:
            with open(VEHICLE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(vehicles)
            print(f"Vehicle '{vehicle_id}' deleted successfully.")
        else:
            print(f"Vehicle ID '{vehicle_id}' not found.")

    except FileNotFoundError:
        print("Vehicle file not found.")

def update_vehicle():
    
    vehicle_id = input("Enter the Vehicle ID to update: ")
    vehicles = []
    found = False

    try:
        with open(VEHICLE_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == vehicle_id:
                    found = True
                    vehicle_type = input("Enter new vehicle type (Car, Truck, Motorcycle): ").capitalize()
                    owner_name = input("Enter new owner's name: ")
                    contact_number = input("Enter new contact number: ")
                    vehicles.append([vehicle_id, vehicle_type, owner_name, contact_number])
                else:
                    vehicles.append(row)

        if found:
            with open(VEHICLE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(vehicles)
            print(f"Vehicle '{vehicle_id}' updated successfully.")
        else:
            print(f"Vehicle ID '{vehicle_id}' not found.")

    except FileNotFoundError:
        print("Vehicle file not found.")

def main():
    """Main function to run the Toll Gate Management System."""
    while True:
        print("\nWelcome to the Toll Gate Management System")
        print("1. Add Vehicle")
        print("2. View Vehicles")
        print("3. Log Vehicle Entry")
        print("4. Log Vehicle Exit")
        print("5. View Toll Logs")
        print("6. Generate Daily Report")
        print("7. Delete Vehicle")
        print("8. Update Vehicle")
        print("9. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            add_vehicle()
        elif choice == '2':
            view_vehicles()
        elif choice == '3':
            vehicle_id = input("Enter the vehicle ID: ")
            log_toll_entry(vehicle_id)
        elif choice == '4':
            vehicle_id = input("Enter the vehicle ID: ")
            distance = float(input("Enter the distance traveled (in km): "))
            vehicle_type = input("Enter the vehicle type (Car, Truck, Motorcycle): ").capitalize()
            log_toll_exit(vehicle_id, vehicle_type, distance)
        elif choice == '5':
            view_toll_logs()
        elif choice == '6':
            generate_daily_report()
        elif choice == '7':
            delete_vehicle()
        elif choice == '8':
            update_vehicle()
        elif choice == '9':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
