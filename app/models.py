"""
Pydantic models for the Fitness Studio Booking API.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
import pytz


class FitnessClass(BaseModel):
    """Model for fitness class data."""
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    date_time: datetime
    instructor: str = Field(..., min_length=1, max_length=100)
    available_slots: int = Field(..., ge=0)
    total_slots: int = Field(..., ge=1)
    timezone: str = "Asia/Kolkata"

    @validator('date_time')
    def validate_future_date(cls, v):
        """Ensure class is in the future."""
        if v < datetime.now(pytz.timezone('Asia/Kolkata')):
            raise ValueError('Class date must be in the future')
        return v

    @validator('available_slots')
    def validate_available_slots(cls, v, values):
        """Ensure available slots don't exceed total slots."""
        if 'total_slots' in values and v > values['total_slots']:
            raise ValueError('Available slots cannot exceed total slots')
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BookingRequest(BaseModel):
    """Model for booking request data."""
    class_id: int = Field(..., gt=0)
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr

    @validator('client_name')
    def validate_client_name(cls, v):
        """Ensure client name contains only letters and spaces."""
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Client name must contain only letters and spaces')
        return v.strip()


class Booking(BaseModel):
    """Model for booking data."""
    id: int
    class_id: int
    class_name: str
    client_name: str
    client_email: str
    booking_date: datetime
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BookingResponse(BaseModel):
    """Model for booking response."""
    booking_id: int
    class_name: str
    client_name: str
    client_email: str
    booking_date: datetime
    message: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ClassesResponse(BaseModel):
    """Model for classes list response."""
    classes: List[FitnessClass]


class BookingsResponse(BaseModel):
    """Model for bookings list response."""
    bookings: List[Booking]


class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str
    detail: Optional[str] = None
    status_code: int 