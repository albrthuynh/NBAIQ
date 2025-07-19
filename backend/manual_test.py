#!/usr/bin/env python3
"""
Manual API Testing Script for NBA IQ App
This script allows you to manually test the API endpoints using actual HTTP requests.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER_DATA = {
    "user_id": "test-user-12345",
    "email": "testuser@example.com", 
    "full_name": "Test User",
    "avatar_url": "https://example.com/avatar.jpg"
}

def test_home_endpoint():
    """Test the home endpoint"""
    print("Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure Flask app is running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_user():
    """Test user creation endpoint"""
    print("\nTesting user creation...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/users",
            json=TEST_USER_DATA,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_user_missing_fields():
    """Test user creation with missing fields"""
    print("\nTesting user creation with missing fields...")
    try:
        incomplete_data = {
            "user_id": "test-user-12345",
            "email": "testuser@example.com"
            # Missing full_name
        }
        response = requests.post(
            f"{BASE_URL}/api/users",
            json=incomplete_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_user_no_auth():
    """Test getting user without authentication"""
    print("\nTesting get user without authentication...")
    try:
        response = requests.get(f"{BASE_URL}/api/users/{TEST_USER_DATA['user_id']}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_user_invalid_auth():
    """Test getting user with invalid authentication"""
    print("\nTesting get user with invalid authentication...")
    try:
        headers = {"Authorization": "Bearer invalid-token-123"}
        response = requests.get(
            f"{BASE_URL}/api/users/{TEST_USER_DATA['user_id']}", 
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all manual tests"""
    print("🚀 Starting Manual API Tests for NBA IQ App")
    print("=" * 50)
    
    tests = [
        ("Home Endpoint", test_home_endpoint),
        ("Create User", test_create_user),
        ("Create User - Missing Fields", test_create_user_missing_fields),
        ("Get User - No Auth", test_get_user_no_auth),
        ("Get User - Invalid Auth", test_get_user_invalid_auth),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
        if success:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    print("📝 Manual API Testing Script")
    print("Make sure your Flask app is running on http://localhost:5000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Testing cancelled.")
        sys.exit(0)
