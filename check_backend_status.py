#!/usr/bin/env python3
"""
Quick Backend Status Checker
Run this to see what's wrong with your backend setup
"""

import os
import sys
from pathlib import Path

def check_files():
    print("📁 Checking File Structure")
    print("=" * 30)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Look for backend folder
    backend_dir = current_dir / "backend"
    if backend_dir.exists():
        print("✅ backend/ folder found")
        
        # Check key files
        files_to_check = [
            "main.py",
            "db.py", 
            "create_tables.py",
            ".env",
            "routers/optimize.py"
        ]
        
        for file_path in files_to_check:
            full_path = backend_dir / file_path
            if full_path.exists():
                print(f"✅ {file_path} exists")
                
                # Check if .env has content
                if file_path == ".env":
                    try:
                        content = full_path.read_text()
                        if "TOMTOM_API_KEY" in content:
                            print("   ✅ .env has TOMTOM_API_KEY")
                        if "OPENWEATHER_API_KEY" in content:
                            print("   ✅ .env has OPENWEATHER_API_KEY") 
                        if "DATABASE_URL" in content:
                            print("   ✅ .env has DATABASE_URL")
                    except:
                        print("   ❌ Cannot read .env file")
                        
            else:
                print(f"❌ {file_path} MISSING")
    else:
        print("❌ backend/ folder not found!")
        print("   Make sure you're in the RouteMonk root directory")

def check_db_file():
    print("\n🔍 Checking db.py Content")
    print("=" * 25)
    
    backend_dir = Path.cwd() / "backend"
    db_file = backend_dir / "db.py"
    
    if db_file.exists():
        content = db_file.read_text()
        if "class Delivery(Base):" in content:
            print("✅ db.py has Delivery model (FIXED VERSION)")
        elif "def get_connection():" in content and "class Delivery" not in content:
            print("❌ db.py is OLD VERSION (needs to be replaced)")
        else:
            print("❌ db.py content unclear")
    else:
        print("❌ db.py not found")

def check_optimize_file():
    print("\n🔍 Checking optimize.py Content") 
    print("=" * 30)
    
    optimize_file = Path.cwd() / "backend" / "routers" / "optimize.py"
    
    if optimize_file.exists():
        content = optimize_file.read_text()
        if "class OptimizeRequest(BaseModel):" in content:
            print("✅ optimize.py has OptimizeRequest model (FIXED VERSION)")
        elif "def optimize_route(city: str," in content:
            print("❌ optimize.py is OLD VERSION (needs to be replaced)")
        else:
            print("❌ optimize.py content unclear")
    else:
        print("❌ optimize.py not found")

if __name__ == "__main__":
    print("🔧 RouteMonk Backend Status Check")
    print("=" * 40)
    
    check_files()
    check_db_file() 
    check_optimize_file()
    
    print("\n" + "=" * 40)
    print("💡 If you see ❌ OLD VERSION messages:")
    print("   → You need to replace those files with the fixed versions")
    print("   → The 500 error will continue until files are fixed")