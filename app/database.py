"""
In-memory database implementation for the Fitness Studio Booking API.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pytz
from .models import FitnessClass, Booking
from .utils import generate_booking_id
from data.seed_data import FITNESS_CLASSES, SAMPLE_CLIENTS, generate_sample_schedule


class InMemoryDatabase:
    """In-memory database for storing fitness classes and bookings."""
    
    def __init__(self):
        self.classes: Dict[int, FitnessClass] = {}
        self.bookings: Dict[int, Booking] = {}
        self.next_booking_id = 1
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize the database with sample data."""
        ist_tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist_tz)
        
        # Generate sample schedule for next 7 days
        schedule = generate_sample_schedule(7)
        
        # Create fitness classes
        class_id = 1
        for class_data in schedule:
            # Parse datetime string and make it timezone-aware
            date_time_str = class_data['date_time']
            if '+' in date_time_str:
                # Already timezone-aware
                date_time = datetime.fromisoformat(date_time_str)
            else:
                # Make it timezone-aware
                date_time = datetime.fromisoformat(date_time_str)
                date_time = ist_tz.localize(date_time)
            
            # Find class template
            class_template = next(
                (c for c in FITNESS_CLASSES if c['name'] == class_data['name']), 
                FITNESS_CLASSES[0]
            )
            
            fitness_class = FitnessClass(
                id=class_id,
                name=class_data['name'],
                date_time=date_time,
                instructor=class_data['instructor'],
                available_slots=class_template['max_capacity'],
                total_slots=class_template['max_capacity'],
                timezone="Asia/Kolkata"
            )
            
            self.classes[class_id] = fitness_class
            class_id += 1
    
    def get_all_classes(self) -> List[FitnessClass]:
        """Get all fitness classes."""
        return list(self.classes.values())
    
    def get_class_by_id(self, class_id: int) -> Optional[FitnessClass]:
        """Get a fitness class by ID."""
        return self.classes.get(class_id)
    
    def update_class_slots(self, class_id: int, available_slots: int):
        """Update available slots for a class."""
        if class_id in self.classes:
            self.classes[class_id].available_slots = available_slots
    
    def create_booking(self, class_id: int, class_name: str, client_name: str, 
                      client_email: str, booking_date: datetime) -> int:
        """Create a new booking."""
        booking_id = self.next_booking_id
        self.next_booking_id += 1
        
        booking = Booking(
            id=booking_id,
            class_id=class_id,
            class_name=class_name,
            client_name=client_name,
            client_email=client_email,
            booking_date=booking_date,
            created_at=datetime.now(pytz.timezone('Asia/Kolkata'))
        )
        
        self.bookings[booking_id] = booking
        return booking_id
    
    def get_bookings_by_email(self, email: str) -> List[Booking]:
        """Get all bookings for a specific email."""
        return [
            booking for booking in self.bookings.values()
            if booking.client_email.lower() == email.lower()
        ]
    
    def check_existing_booking(self, class_id: int, client_email: str) -> bool:
        """Check if a client has already booked a specific class."""
        for booking in self.bookings.values():
            if (booking.class_id == class_id and 
                booking.client_email.lower() == client_email.lower()):
                return True
        return False


# Global database instance
_db_instance = None


def get_db() -> InMemoryDatabase:
    """Get the database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = InMemoryDatabase()
    return _db_instance 