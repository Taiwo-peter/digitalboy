import psycopg2
import os

# Get database URL from environment variable
db_url = os.getenv('DATABASE_URL')

# Connect to PostgreSQL database
conn = psycopg2.connect(db_url)
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
