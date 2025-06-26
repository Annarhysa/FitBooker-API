"""
Main FastAPI application for the Fitness Studio Booking API.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import logging

from .models import (
    ClassesResponse, 
    BookingRequest, 
    BookingResponse, 
    BookingsResponse,
    ErrorResponse
)
from .services import get_fitness_service
from .utils import setup_logging

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Fitness Studio Booking API",
    description="A comprehensive booking API for a fictional fitness studio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get service instance
fitness_service = get_fitness_service()


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "message": "Fitness Studio Booking API",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/classes", response_model=ClassesResponse, tags=["Classes"])
async def get_classes():
    """
    Get all upcoming fitness classes.
    
    Returns a list of all available fitness classes with details including
    name, date/time, instructor, and available slots.
    """
    try:
        classes = fitness_service.get_all_classes()
        return ClassesResponse(classes=classes)
    except Exception as e:
        logger.error(f"Error in get_classes endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve classes. Please try again."
        )


@app.post("/book", response_model=BookingResponse, tags=["Bookings"])
async def book_class(booking_request: BookingRequest):
    """
    Book a fitness class.
    
    Accepts a booking request with class_id, client_name, and client_email.
    Validates availability and creates the booking if slots are available.
    """
    try:
        response = fitness_service.book_class(booking_request)
        return response
    except ValueError as e:
        logger.warning(f"Booking validation error: {str(e)}")
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    except KeyError as e:
        logger.warning(f"Class not found: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in book_class endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create booking. Please try again."
        )


@app.get("/bookings", response_model=BookingsResponse, tags=["Bookings"])
async def get_bookings(email: str = Query(..., description="Client email address")):
    """
    Get all bookings for a specific email address.
    
    Returns all bookings made by the specified email address.
    """
    try:
        bookings = fitness_service.get_bookings_by_email(email)
        return BookingsResponse(bookings=bookings)
    except Exception as e:
        logger.error(f"Error in get_bookings endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve bookings. Please try again."
        )


@app.get("/classes/{class_id}", tags=["Classes"])
async def get_class_details(class_id: int):
    """
    Get detailed information about a specific class.
    
    Returns detailed information about a specific fitness class.
    """
    try:
        fitness_class = fitness_service.get_class_details(class_id)
        if not fitness_class:
            raise HTTPException(
                status_code=404,
                detail=f"Class with ID {class_id} not found"
            )
        return fitness_class
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_class_details endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve class details. Please try again."
        )


@app.get("/classes/{class_id}/availability", tags=["Classes"])
async def check_class_availability(class_id: int):
    """
    Check availability of a specific class.
    
    Returns availability information for a specific fitness class.
    """
    try:
        availability = fitness_service.check_class_availability(class_id)
        return availability
    except Exception as e:
        logger.error(f"Error in check_class_availability endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to check class availability. Please try again."
        )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again.",
            "status_code": 500
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Fitness Studio Booking API starting up...")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Fitness Studio Booking API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 