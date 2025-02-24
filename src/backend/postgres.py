"""Main module for connecting to PostgreSQL database."""

import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Construct absolute path to .env
env_path = Path(__file__).resolve().parent.parent.parent / "env" / ".env"

# Path(__file__).resolve(): gets absolute path of postgres.py
# .parent.parent.parent: Moves three levels up
# / "env" / ".env": Appends /env/.env to the path

# Load the .env file
load_dotenv(env_path)

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

connection = psycopg2.connect(host=db_host, database=db_name, user=db_user,
                              password=db_pass)

# test to see if database is connecting
print('Connected to the database')

cursor = connection.cursor()
cursor.execute('SELECT version()')
db_version = cursor.fetchone()
print(db_version)

cursor.close()
