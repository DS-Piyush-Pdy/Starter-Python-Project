def get_roommate_name():
    roommates_name = []
    print("Enter roommate name (or type 'Done' to finish): ")
    while True:
        name = input("Name: ").title().strip()
        if name == "Done":
            break
        elif name:
            roommates_name.append(name)
        else:
            print("Name cannot be empty!")
    return roommates_name


def collect_expense_details(roommates, total_expected=None, purpose_for_expected=""):

    while True:  # loop until valid total is entered (if expected)
        print("\nEnter contributions by each roommate for the expense:")

        expenses_details = []
        total_entered = 0

        for person in roommates:
            try:
                amount = float(input(f"How much did {person} pay? ₹"))
                expenses_details.append({
                    'Payer': person,
                    'Amount': amount,
                    'Purpose': purpose_for_expected if total_expected else input("Purpose of expense: ").title().strip()
                })
                total_entered += amount
            except ValueError:
                print("Invalid input! Restarting input for all.")
                break  # invalid input → restart whole group input

        # Check total only if expected is set
        if total_expected is not None:
            if round(total_entered, 2) != round(total_expected, 2):
                print("\n❌ ERROR: Can't continue — the total payment doesn't match the expected amount!")
                print(f"Expected: ₹{total_expected:.2f}, but got: ₹{total_entered:.2f}. Please re-enter all contributions.\n")
                continue  # restart loop

        return expenses_details



def split_expenses(roommates, expenses):
    total_paid = {roommate: 0 for roommate in roommates}
    total_share = {roommate: 0 for roommate in roommates}

    num_roommates = len(roommates)

    for expense in expenses:
        payer = expense['Payer']
        amount = expense['Amount']

        # Split equally
        share = amount / num_roommates

        # Track payments
        total_paid[payer] += amount

        # Each roommate owes their share
        for roommate in roommates:
            total_share[roommate] += share

    # Calculate Net Balance
    net_balance = {}
    for roommate in roommates:
        net_balance[roommate] = round(total_paid[roommate] - total_share[roommate], 2)

    return total_paid, total_share, net_balance


def display_summary(total_paid, total_share, net_balance):
    print("\n====== Expense Summary ======")
    print("\nTotal Paid:")
    for person, amount in total_paid.items():
        print(f"{person}: ₹{amount:.2f}")
     
    total_amount_paid = sum(total_paid.values())
    print(f"\nTotal Amount Paid by Everyone: ₹{total_amount_paid:.2f}")

    print("\nTotal Share (What each person owes):")
    for person, amount in total_share.items():
        print(f"{person}: ₹{amount:.2f}")

    print("\nNet Balances:")
    for person, balance in net_balance.items():
        status = "gets back" if balance > 0 else "owes"
        print(f"{person} {status} ₹{abs(balance):.2f}")


def main():
    roommates = get_roommate_name()
    print(f"\nRoommates: {', '.join(roommates)}")

    total_expected = None
    purpose_for_expected = ""

    set_total = input("\nDo you want to set a total amount to be paid for a purpose? (yes/no): ").lower()
    
    if set_total == "yes":
        purpose_for_expected = input("Enter the purpose of the payment: ").title().strip()
        while True:
            try:
                total_expected = float(input(f"Enter the total amount to be paid for '{purpose_for_expected}': ₹"))
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

        expenses = collect_expense_details(roommates, total_expected, purpose_for_expected)

    else:
        expenses = collect_expense_details(roommates)

    # This part is shared — it works for both "yes" and "no"
    print("\nCollected Expenses:")
    for e in expenses:
        print(f"{e['Payer']} paid ₹{e['Amount']:.2f} for {e['Purpose']}")

    total_paid, total_share, net_balance = split_expenses(roommates, expenses)
    display_summary(total_paid, total_share, net_balance)

if __name__ == "__main__":
        main()
