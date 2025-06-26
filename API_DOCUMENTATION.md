# 🏋️ Fitness Studio Booking API Documentation

## Overview

The Fitness Studio Booking API is a comprehensive REST API built with FastAPI that allows clients to view fitness classes, book sessions, and manage their bookings. The API includes timezone management, input validation, and comprehensive error handling.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In a production environment, you would implement JWT tokens or API keys.

## API Endpoints

### 1. Health Check

**GET** `/`

Returns the health status of the API.

**Response:**
```json
{
  "message": "Fitness Studio Booking API",
  "version": "1.0.0",
  "status": "healthy"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/"
```

### 2. Get All Classes

**GET** `/classes`

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

**Example:**
```bash
curl -X GET "http://localhost:8000/classes"
```

### 3. Get Class Details

**GET** `/classes/{class_id}`

Returns detailed information about a specific class.

**Parameters:**
- `class_id` (integer, required): The ID of the class

**Response:**
```json
{
  "id": 1,
  "name": "Yoga",
  "date_time": "2024-01-15T10:00:00+05:30",
  "instructor": "Sarah Johnson",
  "available_slots": 15,
  "total_slots": 20,
  "timezone": "Asia/Kolkata"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/classes/1"
```

### 4. Check Class Availability

**GET** `/classes/{class_id}/availability`

Returns availability information for a specific class.

**Parameters:**
- `class_id` (integer, required): The ID of the class

**Response:**
```json
{
  "available": true,
  "message": "Slots available",
  "available_slots": 15,
  "total_slots": 20,
  "class_name": "Yoga",
  "date_time": "2024-01-15T10:00:00+05:30"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/classes/1/availability"
```

### 5. Book a Class

**POST** `/book`

Books a fitness class for a client.

**Request Body:**
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
  "booking_id": 12345,
  "class_name": "Yoga",
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "booking_date": "2024-01-15T10:00:00+05:30",
  "message": "Booking successful!"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }'
```

### 6. Get Bookings by Email

**GET** `/bookings`

Returns all bookings for a specific email address.

**Query Parameters:**
- `email` (string, required): The client's email address

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "class_id": 1,
      "class_name": "Yoga",
      "client_name": "John Doe",
      "client_email": "john@example.com",
      "booking_date": "2024-01-15T10:00:00+05:30",
      "created_at": "2024-01-10T14:30:00+05:30"
    }
  ]
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/bookings?email=john@example.com"
```

## Data Models

### FitnessClass
```json
{
  "id": "integer",
  "name": "string (1-100 characters)",
  "date_time": "datetime (ISO format)",
  "instructor": "string (1-100 characters)",
  "available_slots": "integer (>= 0)",
  "total_slots": "integer (>= 1)",
  "timezone": "string (default: Asia/Kolkata)"
}
```

### BookingRequest
```json
{
  "class_id": "integer (> 0)",
  "client_name": "string (1-100 characters, letters and spaces only)",
  "client_email": "valid email format"
}
```

### BookingResponse
```json
{
  "booking_id": "integer",
  "class_name": "string",
  "client_name": "string",
  "client_email": "string",
  "booking_date": "datetime (ISO format)",
  "message": "string"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### 400 Bad Request
Invalid request data or missing required fields.

### 404 Not Found
The requested resource (class, booking) was not found.

### 409 Conflict
The class is full or the client has already booked this class.

### 422 Unprocessable Entity
Validation errors (invalid email format, invalid class ID, etc.).

### 500 Internal Server Error
Unexpected server errors.

**Error Response Format:**
```json
{
  "detail": "Error message describing the issue"
}
```

## Timezone Management

- All classes are stored in IST (Asia/Kolkata) timezone
- All datetime responses include timezone information
- The API automatically handles timezone conversions
- Clients can request data in their local timezone

## Validation Rules

### Class Booking
- Class must exist and be in the future
- Class must have available slots
- Client must not have already booked the same class
- Client name must contain only letters and spaces
- Client email must be in valid format

### Email Validation
- Must be a valid email format
- Examples of valid emails: `user@example.com`, `user.name@domain.co.uk`
- Examples of invalid emails: `invalid-email`, `user@`, `@domain.com`

## Rate Limiting

Currently, the API does not implement rate limiting. In production, consider implementing:
- Rate limiting per IP address
- Rate limiting per user account
- Different limits for different endpoints

## Logging

The API includes comprehensive logging:
- All API requests are logged
- Error conditions are logged with details
- Booking operations are logged for audit purposes
- Logs are written to both console and file (`fitness_studio.log`)

## Sample Use Cases

### 1. Client Booking Flow

1. **Get available classes:**
   ```bash
   curl -X GET "http://localhost:8000/classes"
   ```

2. **Check class availability:**
   ```bash
   curl -X GET "http://localhost:8000/classes/1/availability"
   ```

3. **Book the class:**
   ```bash
   curl -X POST "http://localhost:8000/book" \
     -H "Content-Type: application/json" \
     -d '{
       "class_id": 1,
       "client_name": "John Doe",
       "client_email": "john@example.com"
     }'
   ```

4. **View booking history:**
   ```bash
   curl -X GET "http://localhost:8000/bookings?email=john@example.com"
   ```

### 2. Error Handling Examples

**Booking a full class:**
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }'
```
Response: `409 Conflict` - "This class is full. No available slots."

**Booking with invalid email:**
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "invalid-email"
  }'
```
Response: `422 Unprocessable Entity` - Validation error

**Booking non-existent class:**
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 99999,
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }'
```
Response: `404 Not Found` - "Class with ID 99999 not found"

## Testing

The API includes comprehensive test coverage:
- Unit tests for all endpoints
- Service layer tests
- Error handling tests
- Integration tests

Run tests with:
```bash
pytest tests/ -v
```

## Performance Considerations

- The API uses in-memory SQLite for development
- For production, consider using PostgreSQL or MySQL
- Implement database connection pooling
- Add caching for frequently accessed data
- Consider implementing pagination for large datasets

## Security Considerations

- Input validation and sanitization
- SQL injection prevention (using parameterized queries)
- XSS prevention through proper output encoding
- Rate limiting (recommended for production)
- HTTPS enforcement (recommended for production)
- API key authentication (recommended for production)

## Future Enhancements

- User authentication and authorization
- Class cancellation functionality
- Waitlist management
- Payment integration
- Email notifications
- Mobile app support
- Analytics and reporting
- Multi-location support 