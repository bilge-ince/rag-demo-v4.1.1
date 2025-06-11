import os
from db import get_connection


def create_db(args):

    conn = get_connection()
    conn.autocommit = True  # Enable autocommit for creating the database

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT 1 FROM pg_database WHERE datname = '{os.getenv('DB_NAME')}';"
    )
    database_exists = cursor.fetchone()
    cursor.close()

    if not database_exists:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')};")
        cursor.close()
        print("Database created.")

    conn.close()
    # db_config["dbname"] = os.getenv("DB_NAME")
    conn = get_connection()
    print("Connection is successful!")
    conn.autocommit = True

    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS aidb cascade;")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS pgfs;")
    
    cursor.close()
    print("Database setup completed.")
