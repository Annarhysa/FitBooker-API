"""
Tests for the service layer business logic.
"""
import pytest
from datetime import datetime, timedelta
import pytz
from unittest.mock import Mock, patch

from app.models import BookingRequest, FitnessClass
from app.services import FitnessStudioService


class TestFitnessStudioService:
    """Test the FitnessStudioService class."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.service = FitnessStudioService()
    
    def test_get_all_classes(self):
        """Test getting all classes."""
        with patch.object(self.service.db, 'get_all_classes') as mock_get:
            mock_classes = [
                FitnessClass(
                    id=1,
                    name="Yoga",
                    date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
                    instructor="Sarah Johnson",
                    available_slots=20,
                    total_slots=20
                )
            ]
            mock_get.return_value = mock_classes
            
            result = self.service.get_all_classes()
            
            assert result == mock_classes
            mock_get.assert_called_once()
    
    def test_book_class_success(self):
        """Test successful booking."""
        booking_request = BookingRequest(
            class_id=1,
            client_name="John Doe",
            client_email="john@example.com"
        )
        
        mock_class = FitnessClass(
            id=1,
            name="Yoga",
            date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
            instructor="Sarah Johnson",
            available_slots=20,
            total_slots=20
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=mock_class), \
             patch.object(self.service.db, 'check_existing_booking', return_value=False), \
             patch.object(self.service.db, 'create_booking', return_value=12345), \
             patch.object(self.service.db, 'update_class_slots', return_value=True):
            
            result = self.service.book_class(booking_request)
            
            assert result.booking_id == 12345
            assert result.class_name == "Yoga"
            assert result.client_name == "John Doe"
            assert result.client_email == "john@example.com"
            assert "successful" in result.message
    
    def test_book_class_not_found(self):
        """Test booking a non-existent class."""
        booking_request = BookingRequest(
            class_id=999,
            client_name="John Doe",
            client_email="john@example.com"
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=None):
            with pytest.raises(KeyError, match="Class with ID 999 not found"):
                self.service.book_class(booking_request)
    
    def test_book_class_full(self):
        """Test booking a full class."""
        booking_request = BookingRequest(
            class_id=1,
            client_name="John Doe",
            client_email="john@example.com"
        )
        
        mock_class = FitnessClass(
            id=1,
            name="Yoga",
            date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
            instructor="Sarah Johnson",
            available_slots=0,  # Full class
            total_slots=20
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=mock_class):
            with pytest.raises(ValueError, match="This class is full"):
                self.service.book_class(booking_request)
    
    def test_book_class_already_booked(self):
        """Test booking a class that's already booked by the same email."""
        booking_request = BookingRequest(
            class_id=1,
            client_name="John Doe",
            client_email="john@example.com"
        )
        
        mock_class = FitnessClass(
            id=1,
            name="Yoga",
            date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
            instructor="Sarah Johnson",
            available_slots=20,
            total_slots=20
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=mock_class), \
             patch.object(self.service.db, 'check_existing_booking', return_value=True):
            
            with pytest.raises(ValueError, match="already booked"):
                self.service.book_class(booking_request)
    
    def test_get_bookings_by_email(self):
        """Test getting bookings by email."""
        with patch.object(self.service.db, 'get_bookings_by_email') as mock_get:
            mock_bookings = [
                Mock(
                    id=1,
                    class_id=1,
                    class_name="Yoga",
                    client_name="John Doe",
                    client_email="john@example.com",
                    booking_date=datetime.now(pytz.timezone('Asia/Kolkata')),
                    created_at=datetime.now(pytz.timezone('Asia/Kolkata'))
                )
            ]
            mock_get.return_value = mock_bookings
            
            result = self.service.get_bookings_by_email("john@example.com")
            
            assert result == mock_bookings
            mock_get.assert_called_once_with("john@example.com")
    
    def test_get_class_details_found(self):
        """Test getting class details when class exists."""
        mock_class = FitnessClass(
            id=1,
            name="Yoga",
            date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
            instructor="Sarah Johnson",
            available_slots=20,
            total_slots=20
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=mock_class):
            result = self.service.get_class_details(1)
            
            assert result == mock_class
            self.service.db.get_class_by_id.assert_called_once_with(1)
    
    def test_get_class_details_not_found(self):
        """Test getting class details when class doesn't exist."""
        with patch.object(self.service.db, 'get_class_by_id', return_value=None):
            result = self.service.get_class_details(999)
            
            assert result is None
            self.service.db.get_class_by_id.assert_called_once_with(999)
    
    def test_check_class_availability_available(self):
        """Test checking availability for an available class."""
        mock_class = FitnessClass(
            id=1,
            name="Yoga",
            date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
            instructor="Sarah Johnson",
            available_slots=5,
            total_slots=20
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=mock_class):
            result = self.service.check_class_availability(1)
            
            assert result["available"] is True
            assert result["available_slots"] == 5
            assert result["total_slots"] == 20
            assert result["class_name"] == "Yoga"
    
    def test_check_class_availability_full(self):
        """Test checking availability for a full class."""
        mock_class = FitnessClass(
            id=1,
            name="Yoga",
            date_time=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1),
            instructor="Sarah Johnson",
            available_slots=0,
            total_slots=20
        )
        
        with patch.object(self.service.db, 'get_class_by_id', return_value=mock_class):
            result = self.service.check_class_availability(1)
            
            assert result["available"] is False
            assert result["available_slots"] == 0
            assert result["total_slots"] == 20
            assert "full" in result["message"]
    
    def test_check_class_availability_not_found(self):
        """Test checking availability for a non-existent class."""
        with patch.object(self.service.db, 'get_class_by_id', return_value=None):
            result = self.service.check_class_availability(999)
            
            assert result["available"] is False
            assert result["available_slots"] == 0
            assert result["total_slots"] == 0
            assert "not found" in result["message"]


if __name__ == "__main__":
    pytest.main([__file__]) 