from db import Base, engine
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    try:
        # Create tables using SQLAlchemy
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully using SQLAlchemy")
        
        # Verify table exists
        DATABASE_URL = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"✓ Tables in database: {[table for table in tables]}")
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
