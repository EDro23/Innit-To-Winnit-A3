# sales_data.csv file included in ZIP file, also the Sales_data.db.
from dataclasses import dataclass
import sqlite3
import csv
from datetime import datetime


@dataclass
class Region:
    """
    Represents a region in Sales Importer.
    """
    name: str = ""
    code: str = ""
    region: str = ""

    @classmethod
    def get_region_from_code(cls, code):
        """
        Returns the region associated with a given code
        :param code:
        :return: An empty Region object if code is not found
        """
        conn = sqlite3.connect("Sales_data.db")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Region WHERE code = ?''', (code,))
        row = cur.fetchone()
        conn.close()
        if row:
            return cls(name=row[1], code=row[0], region=row[2])
        else:
            return cls()


@dataclass
class DailySales:
    """
    Represents a daily sales in Sales Importer.
    """
    id: int = None
    amount: int = 0
    date: str = ""
    region: Region = None
    quarter: int = 0

    @classmethod
    def from_db(cls, row):
        """
        Creates a new DailySales object from a database row.
        :param row:
        :return: returns a new DailySales object.
        """
        if len(row) >= 7:
            region_data = (row[3], row[4], row[5])
            region = Region(*region_data)
        else:
            region = None
        return cls(id=row[0], amount=row[1], date=row[2], region=region, quarter=row[6])

    @staticmethod
    def get_quarter(date_string):
        """
        Returns the quarter for a given date string
        :param date_string:
        :return: quarter
        """
        if len(date_string) == 4:  # If the date string is just a year
            return 0  # Set the quarter to 0 or handle it accordingly
        else:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            month = date.month
            quarter = (month - 1) // 3 + 1
            return quarter


class DB:
    """
    Represents a database in Sales Importer.
    """

    @staticmethod
    def add_sales(sales, region_code):
        """
        Adds a new sales to the database.
        :param sales: user input sales
        :param region_code: user input code
        :return: None
        """
        conn = sqlite3.connect("Sales_data.db")
        cur = conn.cursor()
        cur.execute('''INSERT INTO Sales (ID, amount, salesDate, region) VALUES (?, ?, ?, ?)''',
                    (sales.id, sales.amount, sales.date, region_code))
        conn.commit()
        conn.close()

    @staticmethod
    def get_or_create_region(region_name):
        """
        Returns the region associated with a given name.
        :param region_name:
        :return: region
        """
        conn = sqlite3.connect("Sales_data.db")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Region WHERE name = ?''', (region_name,))
        row = cur.fetchone()
        if row:
            region = Region(*row)
        else:
            # Insert new region into Region table
            region = Region(name=region_name)
            DB.add_region(region)
        conn.close()
        return region

    @staticmethod
    def import_sales_from_csv(csv_file):
        """
        Imports sales from csv file and returns it as a list.
        :param csv_file:
        :return: none
        """
        try:
            with open(csv_file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    date = row['Date']
                    amount = int(row['Amount'])
                    region_code = row['Region'][0]  # Extract the first character of the region name
                    quarter = int(row['Quarter'])
                    sales = DailySales(amount=amount, date=date)
                    DB.add_sales(sales, region_code)
            print("Imported sales successfully.")
        except Exception as e:
            print("Error:", e)
            print("Import failed.")

    @staticmethod
    def get_all_sales():
        """
        Returns all sales in the database
        :return: sales_list
        """
        conn = sqlite3.connect("Sales_data.db")
        cur = conn.cursor()
        cur.execute('''SELECT Sales.ID, Sales.amount, Sales.salesDate, Region.name as region_name
                        FROM Sales
                        LEFT JOIN Region ON Sales.region = Region.code
                        ORDER BY date(Sales.salesDate)''')
        rows = cur.fetchall()
        sales_list = []
        for row in rows:
            if row[3] is not None:  # Check if region data exists and is not None
                region_data = row[3]
            else:
                region_data = "Unknown"  # If region data is missing or None, set it to "Unknown"
            quarter = DailySales.get_quarter(row[2])  # Calculate quarter based on date
            sales_list.append(DailySales(id=row[0], amount=row[1], date=row[2], region=region_data, quarter=quarter))
        return sales_list

    @staticmethod
    def add_imported_file(file_name):
        """
        Adds a new sales to the database from a CSV file.
        :param file_name:
        :return:
        """
        conn = sqlite3.connect("Sales_data.db")
        cur = conn.cursor()
        cur.execute('''INSERT INTO ImportedFiles (fileName) VALUES (?)''', (file_name,))
        conn.commit()
        conn.close()


class Menu:
    """
    Represents a menu in Sales Importer.
    """

    @staticmethod
    def menu_contents():
        """
        Menu contents for program.
        :return: Menu contents
        """
        print("COMMAND MENU")
        print("view - View all sales")
        print("add - Add sales")
        print("import - Import sales from CSV file")
        print("menu - Show menu")
        print("exit - Exit the program")
        print()


def main():
    """
    Main function for the program
    :return:
    """
    print("SALES DATA IMPORTER")
    print()
    Menu.menu_contents()
    while True:
        user_input = input("Please enter command: ")
        if user_input == "view":
            sales = DB.get_all_sales()
            print("{:<2} {:<12} {:<8} {:<15} {:<15}".format("", "Date", "Quarter", "Region", "Amount"))
            print("-" * 55)
            for i, sale in enumerate(sales, start=1):
                formatted_amount = "${:,.2f}".format(sale.amount)
                print("{:<1}. {:<12} {:<8} {:<15} {:<15}".format(i, sale.date, sale.quarter, sale.region,
                                                                 formatted_amount))
            print("-" * 55)
        elif user_input == "add":
            while True:
                try:
                    amount = int(input("Enter amount: "))
                    while True:
                        try:
                            date = input("Enter date (YYYY-MM-DD): ")
                            if not date:
                                raise ValueError("Date cannot be empty.")
                            datetime.strptime(date, '%Y-%m-%d')  # Validate the date format
                            break  # If the date format is valid, break out of the loop
                        except ValueError:
                            print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                    while True:
                        region_code = input("Enter region code (E, S, N, W): ")
                        if region_code in ['E', 'S', 'N', 'W']:
                            break
                        print("Invalid region code. Please enter a valid region code.")
                    sales = DailySales(amount=amount, date=date)
                    DB.add_sales(sales, region_code)
                    print("Sale added successfully.")
                    break  # Break out of the loop if everything works.
                except ValueError as e:
                    print("Error:", e)
                    print("Please try again.")
        elif user_input == "import":
            try:
                file_name = input("Enter CSV file name: ")
                if not file_name:
                    raise ValueError("File name cannot be empty.")
                DB.import_sales_from_csv(file_name)
                DB.add_imported_file(file_name)
            except Exception as e:
                print("Error:", e)
        elif user_input == "menu":
            Menu.menu_contents()
        elif user_input == "exit":
            print("Bye!")
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
