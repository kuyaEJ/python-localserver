import sqlite3
from sqlite3 import Error
from typing import Any

def create_connection(db_file):
    """Create database connection to the SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        print(f'Connected to SQLite database: {db_file}')
        return conn
    except Error as e:
        print(f'Error connecting to database: {e}')
        return None

def addcolumn(conn, table, name, column_type, constraints):
    """Add a column to a table that exists"""
    try:
        sql_alter = f"""ALTER TABLE {table}
        ADD COLUMN {name} {column_type} {constraints}
        """
        conn.execute(sql_alter)
        conn.commit()
        print(f"Added column {name} to {table}")
    except Error as e:
        if str(e).find("duplicate") == 0:
            pass
        else:
            print(f'Error editing table: {e}')

def create_table(conn, table, constraints):
    """Create a table if it doesn't exist"""
    try:
        # conn.execute("DROP TABLE IF EXISTS links")
        sql_create_table = ""
        if len(constraints) > 0:
            sql_create_table = f"""CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {constraints}
            )
            """
        else:
            sql_create_table = f"""CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """
            
        conn.execute(sql_create_table)
        conn.commit()
        print(f'Table \'{table}\' created or already exists')
    except Error as e:
        print(f'Error creating table: {e}')

def insert(conn, table, vars, vals):
    """Insert a new value into the table"""
    if not vals.strip() or not vars.strip():
        print(f"Values in {table} cannot be empty.")
        return
    try:
        sql_insert = f"INSERT INTO {table} ({vars}) VALUES ({vals})"
        conn.execute(sql_insert)
        conn.commit()
        print(f'Inserted {vals} in {table}.')
    except Error as e:
        print(f'Error inserting value into table {table}: {e}')

def fetch_all(conn, table, vals) -> list[Any]:
    """Fetch all rows from the links table"""
    try:
        cursor = conn.execute(f"SELECT {vals} FROM {table}")
        rows = cursor.fetchall()
        # Gets table name first letter and replaces it with uppercase version
        print(f"{table.replace(table[0], table[0].upper(), 1)} in database:")
        for row in rows:
            print(row)
        return rows
    except Error as e:
        print(f'Error fetching {table}: {e}')
        return []

def remove(conn, table, pkid):
    try:
        sql_delete = f"DELETE FROM {table} WHERE id = ?"
        cursor = conn.execute(sql_delete, (pkid, ))
        if cursor.rowcount > 0:
            print(f'Deleted row with ID {pkid}')
        else:
            print(f'No row found with ID {pkid}')
    except Error as e:
        print(f'Error deleting row: {e}')

def close(conn):
    try:
        conn.close()
        print("Database connection closed.")
    except Error as e:
        print(f'Error deleting connection: {e}')

def main():
    database = 'example.db'

    conn = create_connection(database)
    if conn is None:
        return

    # Create table
    create_table(conn)

    # Insert sample data
    insert(conn, 'links', 'www.google.com', 'Google')
    insert(conn, 'links', 'www.youtube.com', 'YouTube')
    # remove(conn, 'links', 1)
    # remove(conn, 'links', 2)

    fetch_all(conn)
    conn.close()
    print('Database connection closed.')

if __name__ == '__main__':
    main()