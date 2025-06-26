"""
Utility functions for the Fitness Studio Booking API.
"""
import logging
import pytz
from datetime import datetime
from typing import Optional
import os


def setup_logging() -> logging.Logger:
    """Setup structured logging for the application."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('fitness_studio.log')
        ]
    )
    
    return logging.getLogger(__name__)


def get_timezone() -> str:
    """Get the default timezone for the application."""
    return os.getenv('TIMEZONE', 'Asia/Kolkata')


def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """
    Convert datetime from one timezone to another.
    
    Args:
        dt: Datetime object to convert
        from_tz: Source timezone
        to_tz: Target timezone
    
    Returns:
        Converted datetime object
    """
    if dt.tzinfo is None:
        # If datetime is naive, assume it's in the source timezone
        source_tz = pytz.timezone(from_tz)
        dt = source_tz.localize(dt)
    
    target_tz = pytz.timezone(to_tz)
    return dt.astimezone(target_tz)


def format_datetime(dt: datetime, timezone: Optional[str] = None) -> str:
    """
    Format datetime for API responses.
    
    Args:
        dt: Datetime object to format
        timezone: Optional timezone to convert to
    
    Returns:
        Formatted datetime string
    """
    if timezone and dt.tzinfo:
        dt = convert_timezone(dt, str(dt.tzinfo), timezone)
    
    return dt.isoformat()


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if email is valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_string(s: str) -> str:
    """
    Sanitize string input to prevent injection attacks.
    
    Args:
        s: String to sanitize
    
    Returns:
        Sanitized string
    """
    import html
    return html.escape(s.strip())


def generate_booking_id() -> int:
    """
    Generate a unique booking ID.
    In a real application, this would use a database sequence.
    
    Returns:
        Unique booking ID
    """
    import time
    return int(time.time() * 1000)


def is_class_full(available_slots: int) -> bool:
    """
    Check if a class is full.
    
    Args:
        available_slots: Number of available slots
    
    Returns:
        True if class is full, False otherwise
    """
    return available_slots <= 0


def calculate_available_slots(total_slots: int, booked_slots: int) -> int:
    """
    Calculate available slots for a class.
    
    Args:
        total_slots: Total number of slots
        booked_slots: Number of booked slots
    
    Returns:
        Number of available slots
    """
    return max(0, total_slots - booked_slots) 