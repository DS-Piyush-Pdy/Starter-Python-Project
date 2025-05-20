import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv

# Logic Functions
def calculate_balances(roommates, expenses):
    total_paid = {name: 0 for name in roommates}
    total_share = {name: 0 for name in roommates}

    for exp in expenses:
        payer, amount, purpose = exp
        amount = float(amount)
        total_paid[payer] += amount
        share = amount / len(roommates)
        for person in roommates:
            total_share[person] += share

    net_balance = {name: round(total_paid[name] - total_share[name], 2) for name in roommates}
    return total_paid, total_share, net_balance

def get_status(balance):
    if balance > 0:
        return "Gets Back"
    elif balance < 0:
        return "Owes"
    else:
        return "Settled"

# Export Functions
def export_to_txt(data, transactions, filename="balance_sheet.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        total_spent = sum(d['paid'] for d in data.values())
        f.write(f"Total Amount Spent by Everyone: ₹{total_spent:.2f}\n\n")
        f.write("===== Balance Sheet : =====\n\n")
        for name, details in data.items():
            f.write(f"{name}: Paid ₹{details['paid']:.2f}, Share ₹{details['share']:.2f}, "
                    f"Balance ₹{details['balance']:.2f} → {details['status']}\n")
        f.write("\n===== Creditor and Debtor =====\n")
        for t in transactions:
            f.write(f"=> {t}\n")

def export_to_csv(data, transactions, filename="balance_sheet.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Roommate", "Total Paid", "Total Share", "Balance", "Status"])
        for name, details in data.items():
            writer.writerow([name, details['paid'], details['share'], details['balance'], details['status']])
        writer.writerow([])
        writer.writerow(["Transactions"])
        for t in transactions:
            writer.writerow([t])

# GUI App
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roommate Expense Splitter")

        self.roommates = []
        self.expenses = []

        self.setup_ui()

    def setup_ui(self):
        # Roommate Entry
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        self.name_entry = tk.Entry(frame_top)
        self.name_entry.grid(row=0, column=0)
        tk.Button(frame_top, text="Add Roommate", command=self.add_roommate).grid(row=0, column=1)

        self.roommate_listbox = tk.Listbox(frame_top, height=4)
        self.roommate_listbox.grid(row=1, column=0, columnspan=2, pady=5)

        # Expense Entry
        frame_mid = tk.Frame(self.root)
        frame_mid.pack(pady=10)

        self.payer_cb = ttk.Combobox(frame_mid, state="readonly")
        self.payer_cb.grid(row=0, column=0)
        self.amount_entry = tk.Entry(frame_mid)
        self.amount_entry.grid(row=0, column=1)
        self.purpose_entry = tk.Entry(frame_mid)
        self.purpose_entry.grid(row=0, column=2)

        tk.Button(frame_mid, text="Add Expense", command=self.add_expense).grid(row=0, column=3)

        self.expense_tree = ttk.Treeview(self.root, columns=("Payer", "Amount", "Purpose"), show="headings")
        for col in self.expense_tree["columns"]:
            self.expense_tree.heading(col, text=col)
        self.expense_tree.pack(pady=10)

        # Action Buttons
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=10)

        tk.Button(frame_bottom, text="Calculate & Show Summary", command=self.calculate).grid(row=0, column=0, padx=10)
        tk.Button(frame_bottom, text="Export to TXT", command=self.export_txt).grid(row=0, column=1, padx=10)
        tk.Button(frame_bottom, text="Export to CSV", command=self.export_csv).grid(row=0, column=2, padx=10)

    def add_roommate(self):
        name = self.name_entry.get().strip().title()
        if name and name not in self.roommates:
            self.roommates.append(name)
            self.roommate_listbox.insert(tk.END, name)
            self.payer_cb['values'] = self.roommates
            self.name_entry.delete(0, tk.END)

    def add_expense(self):
        payer = self.payer_cb.get()
        amount = self.amount_entry.get().strip()
        purpose = self.purpose_entry.get().strip().title()

        if payer and amount and purpose:
            try:
                float(amount)
                self.expenses.append((payer, amount, purpose))
                self.expense_tree.insert("", tk.END, values=(payer, amount, purpose))
                self.amount_entry.delete(0, tk.END)
                self.purpose_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered.")

    def calculate(self):
        if not self.roommates or not self.expenses:
            messagebox.showwarning("Warning", "Please add roommates and expenses.")
            return

        total_paid, total_share, net_balance = calculate_balances(self.roommates, self.expenses)
        self.summary_data = {}
        self.transactions = []

        creditors = {k: v for k, v in net_balance.items() if v > 0}
        debtors = {k: -v for k, v in net_balance.items() if v < 0}

        for name in self.roommates:
            self.summary_data[name] = {
                "paid": total_paid[name],
                "share": total_share[name],
                "balance": round(abs(net_balance[name]), 2),
                "status": get_status(net_balance[name])
            }

        for debtor, owed_amount in debtors.items():
            for creditor, to_receive in list(creditors.items()):
                if owed_amount == 0:
                    break
                payment = min(owed_amount, to_receive)
                self.transactions.append(f"{debtor} has to give ₹{payment:.2f} to {creditor}")
                owed_amount -= payment
                creditors[creditor] -= payment
                if creditors[creditor] == 0:
                    del creditors[creditor]

        summary = "\n====== Summary ======\n"
        for name, d in self.summary_data.items():
            summary += f"{name}: Paid ₹{d['paid']:.2f}, Share ₹{d['share']:.2f}, Balance ₹{d['balance']:.2f} ({d['status']})\n"
        summary += "\n====== Transactions ======\n" + "\n".join(self.transactions)

        messagebox.showinfo("Summary", summary)

    def export_txt(self):
        if hasattr(self, 'summary_data'):
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if path:
                export_to_txt(self.summary_data, self.transactions, path)

    def export_csv(self):
        if hasattr(self, 'summary_data'):
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if path:
                export_to_csv(self.summary_data, self.transactions, path)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()

