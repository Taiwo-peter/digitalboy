import psycopg2
import os
import time

# Get database URL from environment variable
db_url = os.getenv('DATABASE_URL')

# Function to connect to the PostgreSQL database with retries
def connect_to_db(url):
    while True:
        try:
            conn = psycopg2.connect(url)
            return conn
        except psycopg2.OperationalError:
            print("Database not ready yet, waiting...")
            time.sleep(5)

# Connect to PostgreSQL database
conn = connect_to_db(db_url)
cur = conn.cursor()

# Create the user table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS "user" (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Commit the transaction
conn.commit()

# Close the connection
cur.close()
conn.close()
