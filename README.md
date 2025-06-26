# 🏋️ Fitness Studio Booking API

A comprehensive booking API for a fictional fitness studio built with FastAPI, featuring timezone management, validation, and testing.

## 🚀 Features

- **Class Management**: View all upcoming fitness classes with details
- **Booking System**: Book classes with validation and slot management
- **Booking History**: Retrieve booking history by email
- **Timezone Support**: Automatic timezone conversion (IST to local timezone)
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Proper error responses for edge cases
- **Testing**: Unit tests for all endpoints
- **Logging**: Structured logging for debugging

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (in-memory)
- **Validation**: Pydantic
- **Timezone**: pytz
- **Testing**: pytest
- **Documentation**: Auto-generated with FastAPI

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Omnify
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 📋 API Endpoints

### 1. GET /classes
Returns a list of all upcoming fitness classes.

**Response:**
```json
{
  "classes": [
    {
      "id": 1,
      "name": "Yoga",
      "date_time": "2024-01-15T10:00:00+05:30",
      "instructor": "Sarah Johnson",
      "available_slots": 15,
      "total_slots": 20,
      "timezone": "Asia/Kolkata"
    }
  ]
}
```

### 2. POST /book
Book a class slot.

**Request:**
```json
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```

**Response:**
```json
{
  "booking_id": 1,
  "class_name": "Yoga",
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "booking_date": "2024-01-15T10:00:00+05:30",
  "message": "Booking successful!"
}
```

### 3. GET /bookings?email={email}
Returns all bookings for a specific email address.

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "class_name": "Yoga",
      "client_name": "John Doe",
      "client_email": "john@example.com",
      "booking_date": "2024-01-15T10:00:00+05:30"
    }
  ]
}
```

## 📝 Sample cURL Requests

### Get all classes
```bash
curl -X GET "http://localhost:8000/classes" \
  -H "accept: application/json"
```

### Book a class
```bash
curl -X POST "http://localhost:8000/book" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }'
```

### Get bookings by email
```bash
curl -X GET "http://localhost:8000/bookings?email=john@example.com" \
  -H "accept: application/json"
```

## 🗂️ Project Structure

```
Omnify/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── database.py          # Database operations
│   ├── services.py          # Business logic
│   └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_main.py         # API endpoint tests
│   └── test_services.py     # Service layer tests
├── data/
│   └── seed_data.py         # Sample data
├── requirements.txt
└── README.md
```

## 🌍 Timezone Management

The API handles timezone conversion automatically:
- Classes are stored in IST (Asia/Kolkata)
- All responses include timezone information
- Clients can request data in their local timezone

## 🔧 Configuration

The application uses environment variables for configuration:
- `TIMEZONE`: Default timezone (default: Asia/Kolkata)
- `LOG_LEVEL`: Logging level (default: INFO)

## 🚨 Error Handling

The API provides comprehensive error handling:
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Class or booking not found
- **409 Conflict**: Class is full or already booked
- **422 Unprocessable Entity**: Validation errors

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v --cov=app
```

## 📊 Sample Data

The application comes with pre-loaded sample data including:
- 3 fitness classes (Yoga, Zumba, HIIT)
- Multiple time slots
- Different instructors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 