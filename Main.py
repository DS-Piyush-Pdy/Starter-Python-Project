import csv
from prettytable import PrettyTable


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
    while True:
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
                break

        if total_expected is not None:
            if round(total_entered, 2) != round(total_expected, 2):
                print(f"\n❌ ERROR: Expected: ₹{total_expected:.2f}, but got: ₹{total_entered:.2f}. Please re-enter all contributions.\n")
                continue

        return expenses_details


def split_expenses(roommates, expenses):
    total_paid = {roommate: 0 for roommate in roommates}
    total_share = {roommate: 0 for roommate in roommates}

    num_roommates = len(roommates)

    for expense in expenses:
        payer = expense['Payer']
        amount = expense['Amount']
        share = amount / num_roommates
        total_paid[payer] += amount
        for roommate in roommates:
            total_share[roommate] += share

    net_balance = {}
    for roommate in roommates:
        net_balance[roommate] = round(total_paid[roommate] - total_share[roommate], 2)

    return total_paid, total_share, net_balance


def display_summary(total_paid, total_share, net_balance, export=False):
    total_amount_paid = sum(total_paid.values())
    print(f"\n🧾 Total Amount Spent by Everyone: ₹{total_amount_paid:.2f}\n")

    print("====== Balance Sheet : ======\n")
    table = PrettyTable()
    table.field_names = ["Roommate", "Total Paid (₹)", "Total Share (₹)", "Net Balance (₹)", "Status"]
    data = {}

    for person in total_paid:
        paid = round(total_paid[person], 2)
        share = round(total_share[person], 2)
        net = round(net_balance[person], 2)
        status = "Gets Back" if net > 0 else ("Owes" if net < 0 else "Settled")
        table.add_row([person, f"{paid:.2f}", f"{share:.2f}", f"{abs(net):.2f}", status])
        data[person] = {
            'name': person,
            'paid': paid,
            'share': share,
            'balance': abs(net),
            'status': status,
            'owes': {}
        }

    print(table)

    print("====== Creditor and Debtor ======\n")
    creditors = {k: v for k, v in net_balance.items() if v > 0}
    debtors = {k: -v for k, v in net_balance.items() if v < 0}

    transactions = []

    for debtor, owed_amount in debtors.items():
        for creditor, to_receive in list(creditors.items()):
            if owed_amount == 0:
                break
            payment = min(owed_amount, to_receive)
            transactions.append(f"{debtor} has to give ₹{payment:.2f} to {creditor}")
            data[debtor]['owes'][creditor] = payment
            owed_amount -= payment
            creditors[creditor] -= payment
            if creditors[creditor] == 0:
                del creditors[creditor]

    if transactions:
        for t in transactions:
            print("==>", t)
        print()
    else:
        print("==> Everyone is settled up. No one owes anything!\n")

    if export:
        export_to_txt(data)
        export_to_csv(data)


def export_to_txt(data, filename="balance_sheet.txt"):
    with open(filename, "w",encoding="utf-8") as f:
        total_spent = sum(item['paid'] for item in data.values())
        f.write(f"Total Amount Spent by Everyone: ₹{total_spent:.2f}\n\n")
        f.write("===== Balance Sheet : =====\n\n")
        f.write("+-----------+--------------+----------------+----------------+-------------+\n")
        f.write("| Roommate  | Total Paid (₹)| Total Share (₹)| Net Balance (₹)| Status      |\n")
        f.write("+-----------+--------------+----------------+----------------+-------------+\n")

        for name, details in data.items():
            f.write(f"| {name:<9} | {details['paid']:>12.2f} | {details['share']:>14.2f} | {details['balance']:>14.2f} | {details['status']:<11} |\n")

        f.write("+-----------+--------------+----------------+----------------+-------------+\n\n")
        f.write("===== Creditor and Debtor =====\n\n")

        for item in data.values():
            for to_whom, amount in item.get('owes', {}).items():
                f.write(f"=> {item['name']} has to give ₹{amount:.2f} to {to_whom}\n")


def export_to_csv(data, filename="balance_sheet.csv"):
    with open(filename, mode="w", newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Roommate", "Total Paid (₹)", "Total Share (₹)", "Net Balance (₹)", "Status", "Owes To", "Amount (₹)"])
        for person, details in data.items():
            if details.get("owes"):
                for owed_to, amount in details["owes"].items():
                    writer.writerow([person, f"{details['paid']:.2f}", f"{details['share']:.2f}",
                                     f"{details['balance']:.2f}", details["status"], owed_to, f"{amount:.2f}"])
            else:
                writer.writerow([person, f"{details['paid']:.2f}", f"{details['share']:.2f}",
                                 f"{details['balance']:.2f}", details["status"], "None", "0.00"])


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

    print("\nCollected Expenses:")
    for e in expenses:
        print(f"{e['Payer']} paid ₹{e['Amount']:.2f} for {e['Purpose']}")

    total_paid, total_share, net_balance = split_expenses(roommates, expenses)

    export_choice = input("Do you want to export the balance sheet to TXT/CSV files? (yes/no): ").lower() == "yes"
    display_summary(total_paid, total_share, net_balance, export=export_choice)


if __name__ == "__main__":
    main()

