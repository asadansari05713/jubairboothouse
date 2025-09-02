#!/usr/bin/env python3
"""
Test script for user signup functionality
"""

import requests
import json

def test_user_signup_form():
    """Test user signup with form data"""
    print("Testing user signup with form data...")
    
    url = "http://localhost:8000/auth/user/signup"
    
    # Test data
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
        "whatsapp": "+1234567890"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 201:
            print("✅ Form data signup successful!")
        elif response.status_code == 302:
            print("✅ Form data signup successful (redirect)!")
        else:
            print("❌ Form data signup failed!")
            
    except Exception as e:
        print(f"❌ Error testing form data signup: {e}")

def test_user_signup_json():
    """Test user signup with JSON data"""
    print("\nTesting user signup with JSON data...")
    
    url = "http://localhost:8000/auth/user/signup"
    
    # Test data
    data = {
        "name": "Test User JSON",
        "email": "testjson@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
        "whatsapp": "+1234567890"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ JSON signup successful!")
        else:
            print("❌ JSON signup failed!")
            
    except Exception as e:
        print(f"❌ Error testing JSON signup: {e}")

def test_missing_name_field():
    """Test user signup with missing name field"""
    print("\nTesting user signup with missing name field...")
    
    url = "http://localhost:8000/auth/user/signup"
    
    # Test data without name
    data = {
        "email": "testmissing@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Missing name field properly handled!")
        else:
            print("❌ Missing name field not handled correctly!")
            
    except Exception as e:
        print(f"❌ Error testing missing name field: {e}")

if __name__ == "__main__":
    print("🧪 Testing User Signup Functionality")
    print("=" * 50)
    
    # Note: Make sure the application is running on localhost:8000
    print("Note: Make sure the application is running on localhost:8000")
    print("Run: python run.py")
    print()
    
    test_user_signup_form()
    test_user_signup_json()
    test_missing_name_field()
    
    print("\n" + "=" * 50)
    print("✅ User signup tests completed!")
