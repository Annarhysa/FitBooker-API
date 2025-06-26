"""
Tests for the main FastAPI application endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import pytz

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_root_endpoint(self):
        """Test the root health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Fitness Studio Booking API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"


class TestClassesEndpoint:
    """Test classes endpoint."""
    
    def test_get_classes(self):
        """Test getting all classes."""
        response = client.get("/classes")
        assert response.status_code == 200
        data = response.json()
        assert "classes" in data
        assert isinstance(data["classes"], list)
        
        # Check that classes have required fields
        if data["classes"]:
            class_data = data["classes"][0]
            required_fields = ["id", "name", "date_time", "instructor", "available_slots", "total_slots"]
            for field in required_fields:
                assert field in class_data
    
    def test_get_class_details_valid_id(self):
        """Test getting class details with valid ID."""
        # First get all classes to get a valid ID
        response = client.get("/classes")
        classes = response.json()["classes"]
        
        if classes:
            class_id = classes[0]["id"]
            response = client.get(f"/classes/{class_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == class_id
    
    def test_get_class_details_invalid_id(self):
        """Test getting class details with invalid ID."""
        response = client.get("/classes/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_check_class_availability_valid_id(self):
        """Test checking class availability with valid ID."""
        # First get all classes to get a valid ID
        response = client.get("/classes")
        classes = response.json()["classes"]
        
        if classes:
            class_id = classes[0]["id"]
            response = client.get(f"/classes/{class_id}/availability")
            assert response.status_code == 200
            data = response.json()
            assert "available" in data
            assert "available_slots" in data
            assert "total_slots" in data
    
    def test_check_class_availability_invalid_id(self):
        """Test checking class availability with invalid ID."""
        response = client.get("/classes/99999/availability")
        assert response.status_code == 200
        data = response.json()
        assert data["available"] is False
        assert "not found" in data["message"]


class TestBookingEndpoint:
    """Test booking endpoint."""
    
    def test_book_class_valid_request(self):
        """Test booking a class with valid request."""
        # First get all classes to get a valid ID
        response = client.get("/classes")
        classes = response.json()["classes"]
        
        if classes:
            class_id = classes[0]["id"]
            booking_data = {
                "class_id": class_id,
                "client_name": "John Doe",
                "client_email": "john@example.com"
            }
            
            response = client.post("/book", json=booking_data)
            assert response.status_code == 200
            data = response.json()
            assert "booking_id" in data
            assert data["class_name"] == classes[0]["name"]
            assert data["client_name"] == "John Doe"
            assert data["client_email"] == "john@example.com"
            assert "successful" in data["message"]
    
    def test_book_class_invalid_class_id(self):
        """Test booking a class with invalid class ID."""
        booking_data = {
            "class_id": 99999,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        
        response = client.post("/book", json=booking_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_book_class_invalid_email(self):
        """Test booking a class with invalid email."""
        # First get all classes to get a valid ID
        response = client.get("/classes")
        classes = response.json()["classes"]
        
        if classes:
            class_id = classes[0]["id"]
            booking_data = {
                "class_id": class_id,
                "client_name": "John Doe",
                "client_email": "invalid-email"
            }
            
            response = client.post("/book", json=booking_data)
            assert response.status_code == 422  # Validation error
    
    def test_book_class_missing_fields(self):
        """Test booking a class with missing fields."""
        booking_data = {
            "class_id": 1
            # Missing client_name and client_email
        }
        
        response = client.post("/book", json=booking_data)
        assert response.status_code == 422  # Validation error
    
    def test_book_class_duplicate_booking(self):
        """Test booking the same class twice with same email."""
        # First get all classes to get a valid ID
        response = client.get("/classes")
        classes = response.json()["classes"]
        
        if classes:
            class_id = classes[0]["id"]
            booking_data = {
                "class_id": class_id,
                "client_name": "Jane Doe",
                "client_email": "jane@example.com"
            }
            
            # First booking should succeed
            response = client.post("/book", json=booking_data)
            assert response.status_code == 200
            
            # Second booking with same email should fail
            response = client.post("/book", json=booking_data)
            assert response.status_code == 409
            assert "already booked" in response.json()["detail"]


class TestBookingsEndpoint:
    """Test bookings endpoint."""
    
    def test_get_bookings_valid_email(self):
        """Test getting bookings for valid email."""
        # First create a booking
        response = client.get("/classes")
        classes = response.json()["classes"]
        
        if classes:
            class_id = classes[0]["id"]
            booking_data = {
                "class_id": class_id,
                "client_name": "Alice Smith",
                "client_email": "alice@example.com"
            }
            
            # Create booking
            client.post("/book", json=booking_data)
            
            # Get bookings for the email
            response = client.get("/bookings?email=alice@example.com")
            assert response.status_code == 200
            data = response.json()
            assert "bookings" in data
            assert isinstance(data["bookings"], list)
            
            if data["bookings"]:
                booking = data["bookings"][0]
                assert booking["client_email"] == "alice@example.com"
                assert booking["client_name"] == "Alice Smith"
    
    def test_get_bookings_no_bookings(self):
        """Test getting bookings for email with no bookings."""
        response = client.get("/bookings?email=nonexistent@example.com")
        assert response.status_code == 200
        data = response.json()
        assert "bookings" in data
        assert data["bookings"] == []
    
    def test_get_bookings_missing_email(self):
        """Test getting bookings without email parameter."""
        response = client.get("/bookings")
        assert response.status_code == 422  # Validation error


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        response = client.post("/book", content="invalid json")
        assert response.status_code == 422
    
    def test_method_not_allowed(self):
        """Test method not allowed error."""
        response = client.put("/classes")
        assert response.status_code == 405
    
    def test_not_found(self):
        """Test not found error."""
        response = client.get("/nonexistent")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__]) 