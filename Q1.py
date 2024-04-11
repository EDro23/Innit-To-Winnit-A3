# CSV to Database by Ethan Drover

import sqlite3
import csv


class CSVToDatabase:
    """
    This class reads a CSV file and transfers it to a DB file.
    """

    @staticmethod
    def delete_old_data(db_filename, table_name):
        """
        This method deletes the old data from the database and stores it.
        :param db_filename: DB Input
        :param table_name: Table Input
        :return: None
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Delete old data from the specified table from the user
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def __init__(self):
        pass

    def transfer_data(self, csv_filename, db_filename, table_name):
        """
        This method reads a CSV file and transfers it to a DB
        :param csv_filename: csv input
        :param db_filename: db input
        :param table_name: table input
        :return: -> None
        """
        # Delete old data from the specified table from the user
        self.delete_old_data(db_filename, table_name)

        # Connect to SQLite database
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Read data from CSV and insert into the table inserted by the user
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Map column names from CSV file to corresponding column names in Customer table
                # CSV has different names columns from the DB file.
                mapped_row = {
                    'firstName': row.get('first_name', ''),  # Map 'first_name' from CSV to 'firstName' in database
                    'lastName': row.get('last_name', ''),
                    'companyName': row.get('companyName', ''),
                    'address': row.get('address', ''),
                    'city': row.get('city', ''),
                    'state': row.get('state', ''),
                    'zip': row.get('zip', '')
                }

                # Construct SQL query to insert data
                insert_query = (f"INSERT INTO {table_name} ({', '.join(mapped_row.keys())}) "
                                f"VALUES ({', '.join(['?' for _ in mapped_row.keys()])})")
                cursor.execute(insert_query, tuple(mapped_row.values()))

        # Commit changes and close connection
        conn.commit()
        conn.close()


def main():
    """
    Main function to run the program.
    :return:
    """
    print("Customer Data Importer")
    print()
    csv_filename = input("CSV file (including extension): ")
    db_filename = input("DB file (including extension): ")
    table_name = input("Table name: ")
    print()

    # Instantiate the CSVToDatabase class
    csv_to_db = CSVToDatabase()

    # Transfer data from CSV to the specified table in the database
    csv_to_db.transfer_data(csv_filename, db_filename, table_name)

    print(f"All old rows deleted from {table_name} table.")
    print(f"500 row(s) inserted into {table_name} table.")


if __name__ == "__main__":
    main()
