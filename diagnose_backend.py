#!/usr/bin/env python3
"""
RouteMonk Backend Diagnostic Script
Run this to check what's causing the 500 error
"""

import os
from dotenv import load_dotenv
import requests

def check_environment():
    print("🔍 Checking Environment Variables")
    print("=" * 40)
    
    load_dotenv()
    
    required_vars = [
        "DATABASE_URL",
        "TOMTOM_API_KEY", 
        "OPENWEATHER_API_KEY"
    ]
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if "API_KEY" in var:
                print(f"✅ {var}: {value[:8]}... (hidden)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_good = False
    
    return all_good

def check_database_connection():
    print("\n🗄️ Checking Database Connection")
    print("=" * 40)
    
    try:
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        
        if not DATABASE_URL:
            print("❌ DATABASE_URL not set")
            return False
            
        if DATABASE_URL.startswith("postgresql://"):
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("SELECT 1")
            conn.close()
            print("✅ PostgreSQL database connection working")
            return True
        elif DATABASE_URL.startswith("sqlite://"):
            import sqlite3
            db_path = DATABASE_URL.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
            conn.close()
            print("✅ SQLite database connection working")
            return True
        else:
            print(f"❌ Unknown database type: {DATABASE_URL}")
            return False
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_api_keys():
    print("\n🔑 Checking API Keys")
    print("=" * 30)
    
    load_dotenv()
    
    # Test TomTom API
    tomtom_key = os.getenv("TOMTOM_API_KEY")
    if tomtom_key:
        try:
            url = f"https://api.tomtom.com/routing/1/calculateRoute/52.50931,13.42936:52.50274,13.43872/json?key={tomtom_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ TomTom API key working")
            else:
                print(f"❌ TomTom API key invalid: {response.status_code}")
        except Exception as e:
            print(f"❌ TomTom API test failed: {e}")
    else:
        print("❌ TomTom API key not set")
    
    # Test OpenWeather API  
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    if weather_key:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={weather_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ OpenWeather API key working")
            else:
                print(f"❌ OpenWeather API key invalid: {response.status_code}")
        except Exception as e:
            print(f"❌ OpenWeather API test failed: {e}")
    else:
        print("❌ OpenWeather API key not set")

def check_database_tables():
    print("\n📋 Checking Database Tables")
    print("=" * 35)
    
    try:
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        
        if DATABASE_URL.startswith("postgresql://"):
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [table[0] for table in cur.fetchall()]
            
            if 'deliveries' in tables:
                print("✅ 'deliveries' table exists")
                
                # Check table structure
                cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'deliveries'
                """)
                columns = cur.fetchall()
                print(f"   Columns: {[f'{col[0]} ({col[1]})' for col in columns]}")
            else:
                print("❌ 'deliveries' table missing")
                print(f"   Available tables: {tables}")
                
            conn.close()
            
        elif DATABASE_URL.startswith("sqlite://"):
            import sqlite3
            db_path = DATABASE_URL.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cur.fetchall()]
            
            if 'deliveries' in tables:
                print("✅ 'deliveries' table exists")
            else:
                print("❌ 'deliveries' table missing")
                print(f"   Available tables: {tables}")
                
            conn.close()
            
    except Exception as e:
        print(f"❌ Cannot check database tables: {e}")

if __name__ == "__main__":
    print("🩺 RouteMonk Backend Diagnostics")
    print("=" * 50)
    
    env_ok = check_environment()
    
    if env_ok:
        check_database_connection()
        check_database_tables() 
        check_api_keys()
    else:
        print("\n⚠️  Fix environment variables first!")
    
    print("\n" + "=" * 50)
    print("💡 Next Steps:")
    print("   1. Set up missing environment variables in backend/.env")
    print("   2. Run: python create_tables.py")
    print("   3. Get API keys from TomTom and OpenWeather")
    print("   4. Test again with: python test_backend.py")