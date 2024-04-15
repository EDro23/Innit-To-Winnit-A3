import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from dataclasses import dataclass

@dataclass
class SalesGUI:
    """
    Sales GUI for a sales importer program
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Sales Amount")

        # DB connection, can change to whatever DB.
        self.root.geometry("300x200")
        self.conn = sqlite3.connect("Sales_data.db")
        self.cur = self.conn.cursor()

        # GUI elements
        self.top_label = ttk.Label(self.root, text="Enter date and region to get amount.")
        self.date_label = ttk.Label(root, text="Date:")
        self.date_entry = ttk.Entry(root)
        self.region_label = ttk.Label(root, text="Region:")
        self.region_entry = ttk.Entry(root)
        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_entry = ttk.Entry(root)
        self.id_label = ttk.Label(root, text="ID:")
        self.id_entry = ttk.Entry(root, state="readonly")
        self.save_button = ttk.Button(root, text="Save Changes", command=self.save_changes)
        self.get_amount_button = ttk.Button(root, text="Get Amount", command=self.get_amount)
        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)

        # Grid for the GUI elements
        self.top_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        self.top_label.grid_configure(sticky="ew")
        self.date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.region_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.region_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.amount_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.id_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.id_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.get_amount_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5,sticky="w")
        self.exit_button.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky="e")

    def save_changes(self):
        """
        Retrieve data from entry fields, Update the existing entry and save the changes.
        :return:
        """
        # Retrieve data from entry fields
        ID = int(self.id_entry.get())
        date = self.date_entry.get()
        region = self.region_entry.get()
        amount = float(self.amount_entry.get())

        # Update the existing entry
        self.cur.execute('''UPDATE Sales SET salesDate = ?, region = ?, amount = ? WHERE ID = ?''',
                         (date, region, amount, ID))
        if self.cur.rowcount > 0:
            messagebox.showinfo("Success!", "Sales Amount Updated Successfully! \n:)")
        else:
            messagebox.showinfo("Error", f"No entry found for ID {ID}")

        self.conn.commit()

    def get_amount(self):
        """
        Get amount function for the DB
        :return:
        """
        # Retrieve data from entry fields
        date = self.date_entry.get()
        region = self.region_entry.get()

        # Retrieve amount and ID from the database
        self.cur.execute('''SELECT ID, amount FROM Sales WHERE salesDate = ? AND region = ?''', (date, region))
        row = self.cur.fetchone()
        if row:
            ID, amount = row[0], row[1]
            self.id_entry.config(state="normal")  # Ensure the entry field is editable
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(ID))
            self.id_entry.config(state="readonly")  # Set the entry field back to read-only
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, str(amount))
        else:
            messagebox.showinfo("Error",f"No data found for {date} in {region}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesGUI(root)
    root.mainloop()