import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = psycopg2.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        dbname=os.environ["DB_NAME"],
        port=5432,
    )
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")
