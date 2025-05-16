
# Function to dynamically take roommate names as input
def get_roommate_name():
    roommates_name = []

    print("Enter roommate name (or type 'Done' to finish): ")
    while True:
        name = input("Name: ").title().strip()

        # Stop when user types 'Done'
        if name == "Done":
            break
        elif name:
            roommates_name.append(name) # Add valid name to list
        else:
            print("Name cannot be empty!")

    # Return the list of all roommate names for later processing
    return roommates_name
            


# Function to collect expense details (payer, amount, purpose) and store them as dictionaries in a list
def collect_expense_details():
    expenses_details = []

    print("\nEnter expense details (or type 'Done' to finish): ")

    while True:
        payer = input("Who paid? (or type 'Done' to finish): ").title().strip()

         # Stop when user types 'Done'
        if payer == "Done":
            break

        try: 
            amount = float(input("Amount paid: ₹"))
            purpose = input("Purpose of expense: ").title().strip()

            # Store entry as a dictionary
            expenses_details.append({
                'Payer' : payer,
                'Amount' : amount,
                'Purpose' : purpose
            })

        except ValueError:
            print("Invalid amount. Please Enter a Correct Amount!")

    # Return the full list of expense entries    
    return expenses_details



# Main function to call input functions and print stored data
def main():

    # Collect roommate names
    roommates = get_roommate_name()
    print(f"Roommates: {', '.join(roommates)}")

    # Collect expense entries
    expenses = collect_expense_details()
    print(f"\nCollected Expenses:")
    for e in expenses:
        print(e)

# Ensures this runs only when the script is executed directly
if __name__ == "__main__":
    main()