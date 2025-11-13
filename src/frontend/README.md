# Pet Clinic Frontend

A beautiful Streamlit web application for managing pet clinic appointments.

## Features

- 🏠 **Home Dashboard**: View statistics and recent appointments
- 📅 **Book Appointments**: Easy-to-use form for scheduling pet appointments
- 📋 **View Appointments**: List and manage all appointments with filtering
- 🔍 **Search**: Find appointments by ID
- ✅ **Status Management**: Update appointment status (confirm, complete, cancel)

## Prerequisites

- Python 3.8+
- The appointment-api service running on `http://localhost:8001`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Architecture

```
frontend/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── models/                     # Pydantic models
│   ├── __init__.py
│   ├── animal.py              # Animal model
│   ├── owner.py               # Owner model
│   └── appointment.py         # Appointment models
└── services/                   # API service layer
    ├── __init__.py
    └── appointment_service.py # Appointment API client
```

## API Configuration

By default, the app connects to the appointment API at `http://localhost:8001`. To change this, modify the `base_url` parameter when initializing the `AppointmentService` in `app.py`:

```python
appointment_service = AppointmentService(base_url="http://your-api-url:port")
```

## Usage

### Booking an Appointment

1. Navigate to "📅 Book Appointment"
2. Fill in pet information (name, type, breed, age)
3. Fill in owner information (name, email, phone)
4. Select appointment date and time
5. Provide reason for visit and any additional notes
6. Click "Book Appointment"

### Managing Appointments

1. Navigate to "📋 View Appointments"
2. Filter by status if needed
3. Expand an appointment to view details
4. Use action buttons to:
   - ✅ Confirm the appointment
   - ✔️ Mark as completed
   - 📅 Reschedule (set back to scheduled)
   - ❌ Cancel the appointment

### Searching for an Appointment

1. Navigate to "🔍 Search Appointment"
2. Enter the appointment ID
3. Click "Search" to view details

## Models

All API requests and responses use Pydantic models for type safety and validation:

- `Animal`: Pet information
- `Owner`: Owner contact details
- `AppointmentCreate`: Data for creating new appointments
- `Appointment`: Complete appointment information with ID and status
- `AppointmentStatus`: Enum for appointment states (scheduled, confirmed, completed, cancelled)

## Service Layer

The `AppointmentService` class handles all API communication:

- `create_appointment()`: Create new appointment
- `list_appointments()`: Get all appointments (with optional status filter)
- `get_appointment()`: Get specific appointment by ID
- `update_appointment_status()`: Update appointment status
- `cancel_appointment()`: Cancel and delete appointment

## Styling

The app includes custom CSS for a modern, pet-friendly design with:
- Color-coded status badges
- Responsive layout
- Animal emojis for visual appeal
- Clean card-based design
