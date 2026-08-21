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

def addrow(conn, table, name, type, constraints):
    """Add a column to a table that exists"""
    try:
        sql_alter = """
        ALTER TABLE """ + table + """
        ADD COLUMN """ + name + " " + type + " " + constraints
        conn.execute(sql_alter)
        conn.commit()
        print(f"Added column {name} to {table}")
    except Error as e:
        if str(e).find("duplicate") == 0:
            pass
        else:
            print(f'Error editing table: {e}')

def create_table(conn, table):
    """Create a table if it doesn't exist"""
    try:
        # conn.execute("DROP TABLE IF EXISTS links")
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS """ + table + """ (
        id INTEGER PRIMARY KEY AUTOINCREMENT)
        """
        conn.execute(sql_create_table)
        conn.commit()
        print(f'Table {table} created or already exists')
    except Error as e:
        print(f'Error creating table: {e}')

def insert(conn, table, vars, vals):
    """Insert a new link into the link table"""
    if not vals.strip() or not vars.strip():
        print(f"Values in {table} cannot be empty.")
        return
    try:
        sql_insert = f"INSERT INTO {table} ({vars}) VALUES ({vals})"
        conn.execute(sql_insert)
        conn.commit()
        print(f'Inserted {vals} in {table}.')
    except Error as e:
        print(f'Error inserting link: {e}')

def fetch_all(conn, table) -> list[Any]:
    """Fetch all rows from the links table"""
    try:
        cursor = conn.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        print(f"{table.replace(table[0], table[0].upper(), 1)} in database:")
        for row in rows:
            print(row)
        return rows
    except Error as e:
        print(f'Error fetching {table}: {e}')
        return []

def remove(conn, table, link_id):
    try:
        sql_delete = f"DELETE FROM {table} WHERE id = ?"
        cursor = conn.execute(sql_delete, (link_id, ))
        if cursor.rowcount > 0:
            print(f'Deleted row with ID {link_id}')
        else:
            print(f'No row found with ID {link_id}')
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