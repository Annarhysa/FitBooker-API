#!/usr/bin/env python3
"""
Simple test script to verify the Fitness Studio Booking API functionality.
"""
import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['message']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running.")
        return False

def test_get_classes():
    """Test getting all classes."""
    print("\n📚 Testing get classes...")
    try:
        response = requests.get(f"{BASE_URL}/classes")
        if response.status_code == 200:
            data = response.json()
            classes = data.get('classes', [])
            print(f"✅ Found {len(classes)} classes")
            for i, class_info in enumerate(classes[:3], 1):
                print(f"   {i}. {class_info['name']} - {class_info['instructor']} - {class_info['available_slots']} slots")
            return classes
        else:
            print(f"❌ Get classes failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting classes: {e}")
        return []

def test_book_class(classes):
    """Test booking a class."""
    if not classes:
        print("❌ No classes available for booking test")
        return None
    
    print(f"\n📅 Testing book class...")
    class_info = classes[0]
    
    booking_data = {
        "class_id": class_info['id'],
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/book", json=booking_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Booking successful: {data['message']}")
            print(f"   Booking ID: {data['booking_id']}")
            print(f"   Class: {data['class_name']}")
            return data['booking_id']
        else:
            print(f"❌ Booking failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error booking class: {e}")
        return None

def test_get_bookings():
    """Test getting bookings by email."""
    print(f"\n📋 Testing get bookings...")
    try:
        response = requests.get(f"{BASE_URL}/bookings?email=test@example.com")
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('bookings', [])
            print(f"✅ Found {len(bookings)} bookings for test@example.com")
            for booking in bookings:
                print(f"   - {booking['class_name']} on {booking['booking_date']}")
            return True
        else:
            print(f"❌ Get bookings failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting bookings: {e}")
        return False

def test_class_details(classes):
    """Test getting class details."""
    if not classes:
        print("❌ No classes available for details test")
        return False
    
    print(f"\n🔍 Testing class details...")
    class_info = classes[0]
    
    try:
        response = requests.get(f"{BASE_URL}/classes/{class_info['id']}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Class details retrieved: {data['name']}")
            print(f"   Instructor: {data['instructor']}")
            print(f"   Available slots: {data['available_slots']}/{data['total_slots']}")
            return True
        else:
            print(f"❌ Get class details failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting class details: {e}")
        return False

def test_class_availability(classes):
    """Test checking class availability."""
    if not classes:
        print("❌ No classes available for availability test")
        return False
    
    print(f"\n📊 Testing class availability...")
    class_info = classes[0]
    
    try:
        response = requests.get(f"{BASE_URL}/classes/{class_info['id']}/availability")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Availability checked: {data['class_name']}")
            print(f"   Available: {data['available']}")
            print(f"   Slots: {data['available_slots']}/{data['total_slots']}")
            return True
        else:
            print(f"❌ Check availability failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking availability: {e}")
        return False

def test_error_handling():
    """Test error handling."""
    print(f"\n🚨 Testing error handling...")
    
    # Test booking non-existent class
    try:
        response = requests.post(f"{BASE_URL}/book", json={
            "class_id": 99999,
            "client_name": "Test User",
            "client_email": "test@example.com"
        })
        if response.status_code == 404:
            print("✅ 404 error handled correctly for non-existent class")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing 404: {e}")
    
    # Test invalid email
    try:
        response = requests.post(f"{BASE_URL}/book", json={
            "class_id": 1,
            "client_name": "Test User",
            "client_email": "invalid-email"
        })
        if response.status_code == 422:
            print("✅ 422 error handled correctly for invalid email")
        else:
            print(f"❌ Expected 422, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing 422: {e}")

def main():
    """Main test function."""
    print("🧪 Fitness Studio Booking API Test Suite")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Get Classes", lambda: test_get_classes()),
        ("Class Details", lambda: test_class_details(test_get_classes())),
        ("Class Availability", lambda: test_class_availability(test_get_classes())),
        ("Book Class", lambda: test_book_class(test_get_classes())),
        ("Get Bookings", test_get_bookings),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result is not False))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API implementation.")

if __name__ == "__main__":
    main() 