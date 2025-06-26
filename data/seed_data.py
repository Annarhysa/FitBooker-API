"""
Sample data for the Fitness Studio Booking API.
This file contains sample fitness classes and instructors.
"""
from datetime import datetime, timedelta
import pytz

# Sample instructors
INSTRUCTORS = [
    {
        "name": "Sarah Johnson",
        "specialties": ["Yoga", "Pilates", "Meditation"],
        "experience": "8 years",
        "certifications": ["RYT-500", "Pilates Mat", "Meditation Teacher"]
    },
    {
        "name": "Maria Rodriguez",
        "specialties": ["Zumba", "Latin Dance", "Cardio"],
        "experience": "5 years",
        "certifications": ["Zumba Basic", "Zumba Toning", "Latin Dance Instructor"]
    },
    {
        "name": "Mike Chen",
        "specialties": ["HIIT", "Strength Training", "CrossFit"],
        "experience": "6 years",
        "certifications": ["NASM CPT", "CrossFit Level 2", "HIIT Specialist"]
    },
    {
        "name": "Emma Wilson",
        "specialties": ["Spinning", "Cycling", "Endurance Training"],
        "experience": "4 years",
        "certifications": ["Spinning Instructor", "Cycling Coach", "Endurance Specialist"]
    },
    {
        "name": "David Thompson",
        "specialties": ["Boxing", "Kickboxing", "Self-Defense"],
        "experience": "10 years",
        "certifications": ["Boxing Coach", "Kickboxing Instructor", "Self-Defense Expert"]
    }
]

# Sample fitness classes
FITNESS_CLASSES = [
    {
        "name": "Yoga Flow",
        "description": "A dynamic vinyasa flow class that builds strength and flexibility",
        "duration": 60,
        "difficulty": "Beginner to Intermediate",
        "max_capacity": 20,
        "instructor": "Sarah Johnson"
    },
    {
        "name": "Zumba Fitness",
        "description": "High-energy dance fitness class with Latin rhythms",
        "duration": 45,
        "difficulty": "All Levels",
        "max_capacity": 25,
        "instructor": "Maria Rodriguez"
    },
    {
        "name": "HIIT Circuit",
        "description": "High-intensity interval training with strength and cardio",
        "duration": 30,
        "difficulty": "Intermediate to Advanced",
        "max_capacity": 15,
        "instructor": "Mike Chen"
    },
    {
        "name": "Spinning",
        "description": "Indoor cycling class with music and motivation",
        "duration": 45,
        "difficulty": "All Levels",
        "max_capacity": 18,
        "instructor": "Emma Wilson"
    },
    {
        "name": "Boxing Basics",
        "description": "Learn boxing fundamentals and get a great workout",
        "duration": 60,
        "difficulty": "Beginner",
        "max_capacity": 12,
        "instructor": "David Thompson"
    },
    {
        "name": "Pilates Mat",
        "description": "Core strengthening and body awareness through Pilates",
        "duration": 45,
        "difficulty": "All Levels",
        "max_capacity": 16,
        "instructor": "Sarah Johnson"
    },
    {
        "name": "Kickboxing",
        "description": "High-energy kickboxing class for cardio and strength",
        "duration": 60,
        "difficulty": "Intermediate",
        "max_capacity": 14,
        "instructor": "David Thompson"
    },
    {
        "name": "Latin Dance",
        "description": "Learn salsa, bachata, and merengue moves",
        "duration": 60,
        "difficulty": "Beginner to Intermediate",
        "max_capacity": 20,
        "instructor": "Maria Rodriguez"
    }
]

# Sample time slots
TIME_SLOTS = [
    "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00"
]

# Sample clients for testing
SAMPLE_CLIENTS = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-0101",
        "membership_type": "Premium"
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-555-0102",
        "membership_type": "Standard"
    },
    {
        "name": "Mike Johnson",
        "email": "mike.johnson@example.com",
        "phone": "+1-555-0103",
        "membership_type": "Premium"
    },
    {
        "name": "Sarah Wilson",
        "email": "sarah.wilson@example.com",
        "phone": "+1-555-0104",
        "membership_type": "Standard"
    },
    {
        "name": "David Brown",
        "email": "david.brown@example.com",
        "phone": "+1-555-0105",
        "membership_type": "Premium"
    }
]

# Sample bookings for testing
SAMPLE_BOOKINGS = [
    {
        "class_id": 1,
        "client_name": "John Doe",
        "client_email": "john.doe@example.com",
        "booking_date": "2024-01-15T10:00:00+05:30"
    },
    {
        "class_id": 2,
        "client_name": "Jane Smith",
        "client_email": "jane.smith@example.com",
        "booking_date": "2024-01-15T14:00:00+05:30"
    },
    {
        "class_id": 3,
        "client_name": "Mike Johnson",
        "client_email": "mike.johnson@example.com",
        "booking_date": "2024-01-15T18:00:00+05:30"
    }
]


def generate_sample_schedule(days_ahead=7):
    """
    Generate a sample class schedule for the next N days.
    
    Args:
        days_ahead: Number of days to generate schedule for
        
    Returns:
        List of class schedules
    """
    ist_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist_tz)
    schedule = []
    
    for day in range(1, days_ahead + 1):
        class_date = now + timedelta(days=day)
        
        # Morning classes (6 AM - 12 PM)
        morning_times = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00"]
        for time_slot in morning_times[:3]:  # Limit to 3 morning classes per day
            hour, minute = map(int, time_slot.split(":"))
            class_datetime = class_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            schedule.append({
                "name": "Yoga Flow",
                "date_time": class_datetime.isoformat(),
                "instructor": "Sarah Johnson",
                "available_slots": 20,
                "total_slots": 20
            })
        
        # Afternoon classes (2 PM - 6 PM)
        afternoon_times = ["14:00", "15:00", "16:00", "17:00"]
        for time_slot in afternoon_times[:2]:  # Limit to 2 afternoon classes per day
            hour, minute = map(int, time_slot.split(":"))
            class_datetime = class_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            schedule.append({
                "name": "Zumba Fitness",
                "date_time": class_datetime.isoformat(),
                "instructor": "Maria Rodriguez",
                "available_slots": 25,
                "total_slots": 25
            })
        
        # Evening classes (6 PM - 9 PM)
        evening_times = ["18:00", "19:00", "20:00"]
        for time_slot in evening_times[:2]:  # Limit to 2 evening classes per day
            hour, minute = map(int, time_slot.split(":"))
            class_datetime = class_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            schedule.append({
                "name": "HIIT Circuit",
                "date_time": class_datetime.isoformat(),
                "instructor": "Mike Chen",
                "available_slots": 15,
                "total_slots": 15
            })
    
    return schedule


def get_instructor_by_name(name):
    """
    Get instructor details by name.
    
    Args:
        name: Instructor name
        
    Returns:
        Instructor details or None if not found
    """
    for instructor in INSTRUCTORS:
        if instructor["name"] == name:
            return instructor
    return None


def get_class_by_name(name):
    """
    Get class details by name.
    
    Args:
        name: Class name
        
    Returns:
        Class details or None if not found
    """
    for class_info in FITNESS_CLASSES:
        if class_info["name"] == name:
            return class_info
    return None


if __name__ == "__main__":
    # Print sample data for reference
    print("=== Sample Instructors ===")
    for instructor in INSTRUCTORS:
        print(f"- {instructor['name']}: {', '.join(instructor['specialties'])}")
    
    print("\n=== Sample Classes ===")
    for class_info in FITNESS_CLASSES:
        print(f"- {class_info['name']}: {class_info['description']}")
    
    print("\n=== Sample Schedule (Next 3 days) ===")
    schedule = generate_sample_schedule(3)
    for i, class_schedule in enumerate(schedule[:10], 1):
        print(f"{i}. {class_schedule['name']} - {class_schedule['date_time']} - {class_schedule['instructor']}") 