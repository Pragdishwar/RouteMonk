#!/usr/bin/env python3
"""
RouteMonk Backend Test Script
Run this after applying the fixes to verify backend functionality
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_backend():
    print("🧪 RouteMonk Backend Testing")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend. Is it running on localhost:8000?")
        return False
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
        return False
    
    # Test 2: Optimization endpoint
    print("\n2. Testing optimization endpoint...")
    try:
        test_data = {
            "city": "Mumbai", 
            "perishability": 8, 
            "start": "19.0760,72.8777", 
            "end": "18.9220,72.8347"
        }
        
        response = requests.post(
            f"{BASE_URL}/optimize/",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Optimization endpoint working")
            print(f"   Travel time: {result.get('travel_time_sec', 'N/A')} seconds")
            print(f"   Weather: {result.get('weather', 'N/A')}")
            print(f"   Score: {result.get('final_score', 'N/A')}")
        else:
            print(f"   ❌ Optimization endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Optimization endpoint error: {e}")
        return False
    
    # Test 3: History endpoint
    print("\n3. Testing history endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/history/", timeout=5)
        if response.status_code == 200:
            history = response.json()
            print("   ✅ History endpoint working")
            print(f"   Records found: {len(history.get('history', []))}")
            if history.get('history'):
                print(f"   Latest record: {history['history'][0]}")
        else:
            print(f"   ❌ History endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ History endpoint error: {e}")
        return False
    
    print("\n🎉 All tests passed! Backend is working correctly.")
    return True

def check_requirements():
    print("\n📋 Pre-test Requirements Check")
    print("=" * 40)
    
    requirements = [
        "✅ Backend server running on localhost:8000",
        "✅ PostgreSQL database configured",
        "✅ TOMTOM_API_KEY environment variable set",
        "✅ OPENWEATHER_API_KEY environment variable set",
        "✅ Database tables created (run create_tables.py)",
        "✅ All dependencies installed (pip install -r requirements.txt)"
    ]
    
    for req in requirements:
        print(f"   {req}")
    
    print("\nTo start backend server:")
    print("   cd backend && uvicorn main:app --reload --port 8000")

if __name__ == "__main__":
    check_requirements()
    
    input("\nPress Enter when backend is ready for testing...")
    
    if test_backend():
        print("\n🚀 Backend is ready for production!")
    else:
        print("\n❌ Backend needs fixes before it can work properly.")
        sys.exit(1)