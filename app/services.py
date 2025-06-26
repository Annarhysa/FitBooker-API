"""
Business logic services for the Fitness Studio Booking API.
"""
from datetime import datetime
from typing import List, Optional
import pytz
from .models import FitnessClass, Booking, BookingRequest, BookingResponse
from .database import get_db
from .utils import setup_logging, is_class_full, calculate_available_slots

logger = setup_logging()


class FitnessStudioService:
    """Service class for fitness studio operations."""
    
    def __init__(self):
        self.db = get_db()
    
    def get_all_classes(self) -> List[FitnessClass]:
        """
        Get all upcoming fitness classes.
        
        Returns:
            List of fitness classes
        """
        try:
            classes = self.db.get_all_classes()
            logger.info(f"Successfully retrieved {len(classes)} classes")
            return classes
        except Exception as e:
            logger.error(f"Error retrieving classes: {str(e)}")
            raise
    
    def book_class(self, booking_request: BookingRequest) -> BookingResponse:
        """
        Book a fitness class.
        
        Args:
            booking_request: Booking request data
            
        Returns:
            Booking response with confirmation details
            
        Raises:
            ValueError: If class is full or already booked
            KeyError: If class not found
        """
        try:
            # Get the class details
            fitness_class = self.db.get_class_by_id(booking_request.class_id)
            if not fitness_class:
                logger.warning(f"Class {booking_request.class_id} not found")
                raise KeyError(f"Class with ID {booking_request.class_id} not found")
            
            # Check if class is full
            if is_class_full(fitness_class.available_slots):
                logger.warning(f"Class {booking_request.class_id} is full")
                raise ValueError("This class is full. No available slots.")
            
            # Check if client has already booked this class
            if self.db.check_existing_booking(booking_request.class_id, booking_request.client_email):
                logger.warning(f"Client {booking_request.client_email} already booked class {booking_request.class_id}")
                raise ValueError("You have already booked this class.")
            
            # Create the booking
            booking_id = self.db.create_booking(
                class_id=booking_request.class_id,
                class_name=fitness_class.name,
                client_name=booking_request.client_name,
                client_email=booking_request.client_email,
                booking_date=fitness_class.date_time
            )
            
            # Update available slots
            new_available_slots = fitness_class.available_slots - 1
            self.db.update_class_slots(booking_request.class_id, new_available_slots)
            
            # Create response
            response = BookingResponse(
                booking_id=booking_id,
                class_name=fitness_class.name,
                client_name=booking_request.client_name,
                client_email=booking_request.client_email,
                booking_date=fitness_class.date_time,
                message="Booking successful!"
            )
            
            logger.info(f"Successfully created booking {booking_id} for class {booking_request.class_id}")
            return response
            
        except (ValueError, KeyError):
            # Re-raise these specific exceptions
            raise
        except Exception as e:
            logger.error(f"Error creating booking: {str(e)}")
            raise ValueError("Failed to create booking. Please try again.")
    
    def get_bookings_by_email(self, email: str) -> List[Booking]:
        """
        Get all bookings for a specific email address.
        
        Args:
            email: Client email address
            
        Returns:
            List of bookings for the email
        """
        try:
            bookings = self.db.get_bookings_by_email(email)
            logger.info(f"Successfully retrieved {len(bookings)} bookings for {email}")
            return bookings
        except Exception as e:
            logger.error(f"Error retrieving bookings for {email}: {str(e)}")
            raise
    
    def get_class_details(self, class_id: int) -> Optional[FitnessClass]:
        """
        Get detailed information about a specific class.
        
        Args:
            class_id: Class ID
            
        Returns:
            Fitness class details or None if not found
        """
        try:
            fitness_class = self.db.get_class_by_id(class_id)
            if fitness_class:
                logger.info(f"Retrieved details for class {class_id}")
            else:
                logger.warning(f"Class {class_id} not found")
            return fitness_class
        except Exception as e:
            logger.error(f"Error retrieving class {class_id}: {str(e)}")
            raise
    
    def check_class_availability(self, class_id: int) -> dict:
        """
        Check availability of a specific class.
        
        Args:
            class_id: Class ID
            
        Returns:
            Dictionary with availability information
        """
        try:
            fitness_class = self.db.get_class_by_id(class_id)
            if not fitness_class:
                return {
                    "available": False,
                    "message": "Class not found",
                    "available_slots": 0,
                    "total_slots": 0
                }
            
            is_available = not is_class_full(fitness_class.available_slots)
            
            return {
                "available": is_available,
                "message": "Class is full" if not is_available else "Slots available",
                "available_slots": fitness_class.available_slots,
                "total_slots": fitness_class.total_slots,
                "class_name": fitness_class.name,
                "date_time": fitness_class.date_time
            }
            
        except Exception as e:
            logger.error(f"Error checking availability for class {class_id}: {str(e)}")
            raise


# Global service instance
fitness_service = FitnessStudioService()


def get_fitness_service() -> FitnessStudioService:
    """Get the fitness studio service instance."""
    return fitness_service 