import MySQLdb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

DB_NAME = os.getenv('DB_NAME', 'EKisan_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

print(f"Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER}...")

try:
    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    print(f"Creating database '{DB_NAME}' if it does not exist...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    print("Database created or already exists.")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error creating database: {e}")
    exit(1)
