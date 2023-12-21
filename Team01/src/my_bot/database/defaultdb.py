import os
import sqlite3


"""
Module for interacting with SQLite databases.

Classes:
    DefaultDatabase: Provides basic operations for working with a database.
"""


class DefaultDatabase:
    """Provides basic operations for working with a database.

    Attributes:
        db_name (str): name of database.
        db_exists (bool): .

    Methods:
        __init__(self, db_name="default.db"): Establishes a connection to the database.
        create_tables(self, table_name, *args): Creates a table in the database.
        insert_data(self, table_name, data): Inserts a record into the table.
        insert_or_replace_data(self, table_name, data): Inserts or replaces a record in the table.
        get_all_data(self, table_name): Retrieves all records from the table.
        delete_row(self, table_name, condition): Deletes a record from the table based on the specified condition.
        clear_table(self, table_name): Clears all records from the table.
        drop_table(self, table_name): Drops the specified table from the database.
        drop_database(self): Drops the entire database.
    """
    def __init__(self, db_name="default.db"):
        """
        Establishes a connection to the database.

        Args:
            db_name (str): The name of the database.
        """
        self.db_name = db_name
        self.db_exists = os.path.exists(self.db_name)
        self.connect_db = sqlite3.connect(self.db_name)

    def create_tables(self, table_name, *args):
        """
        Creates a table in the database.

        Args:
            table_name (str): The name of the table.
            *args: Column names and their data types.
        """
        cursor = self.connect_db.cursor()
        columns = ", ".join(args)
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY, 
                {columns}
            )
        """
        cursor.execute(query)
        self.connect_db.commit()

    def insert_data(self, table_name, data):
        """
        Inserts a record into the table.

        Args:
            table_name (str): The name of the table.
            data (dict): Dictionary representing the record to be inserted.
        """
        cursor = self.connect_db.cursor()
        columns = ", ".join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query= f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})

        """
        values = tuple(data.values())
        cursor.execute(query, values)
        self.connect_db.commit()

    def insert_or_replace_data(self, table_name, data):
        """
        Inserts or replaces a record in the table.

        Args:
            table_name (str): The name of the table.
            data (dict): Dictionary representing the record to be inserted or replaced.
        """
        cursor = self.connect_db.cursor()
        columns = ", ".join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query= f"""
            INSERT OR REPLACE INTO {table_name} ({columns})
            VALUES ({placeholders})

        """
        values = tuple(data.values())
        cursor.execute(query, values)
        self.connect_db.commit()

    def get_all_data(self, table_name):
        """
        Retrieves all records from the table.

        Args:
            table_name (str): The name of the table.

        Returns:
            List of tuples representing the records.
        """
        cursor = self.connect_db.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def delete_row(self, table_name, condition):
        """
        Deletes a record from the table based on the specified condition.

        Args:
            table_name (str): The name of the table.
            condition (str): The condition for deleting records.
        """
        cursor = self.connect_db.cursor()
        query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(query)
        self.connect_db.commit()

    def clear_table(self, table_name):
        """
        Clears all records from the table.

        Args:
            table_name (str): The name of the table.
        """
        cursor = self.connect_db.cursor()
        query = f"DELETE FROM {table_name}"
        cursor.execute(query)
        self.connect_db.commit()

    def drop_table(self, table_name):
        """
        Drops the specified table from the database.

        Args:
            table_name (str): The name of the table.
        """
        cursor = self.connect_db.cursor()
        query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(query)
        self.connect_db.commit()

    def drop_database(self):
        """Drops the entire database."""
        self.connect_db.close()
        if os.path.exists(self.db_name):
            os.remove(self.db_name)


if __name__ == "__main__":
    def_db = DefaultDatabase("game.db")
    # print(def_db.get_all_data("user"))
