# Pet Clinic Frontend

A modern web interface for the Pet Clinic Appointment API built with Express, EJS templates, and Dapr.

## Features

- 🔐 **Fake Login System**: Any email/password combination works for demo purposes
- 📅 **Appointment Management**: Create, view, and cancel pet appointments
- 👤 **User Dashboard**: View personal appointments and book new ones
- 🛡️ **Admin Panel**: Special access for `admin@petclinic.com` to charge appointments
- 🐾 **Pet Information**: Support for multiple animal types (dog, cat, bird, rabbit, hamster, other)
- 🔌 **Dapr Integration**: All API calls use Dapr client for service invocation

## Project Structure

```
frontend/
├── models/                    # Data models matching OpenAPI spec
│   ├── Animal.js
│   ├── AnimalType.js
│   ├── Owner.js
│   ├── Appointment.js
│   ├── AppointmentCreate.js
│   └── AppointmentSummary.js
├── services/                  # API service layer
│   └── PetClinicService.js   # Dapr client integration
├── views/                     # EJS templates
│   ├── login.ejs             # Login page
│   ├── dashboard.ejs         # User dashboard
│   ├── admin.ejs             # Admin panel
│   └── appointment-detail.ejs # Appointment details
├── server.js                  # Express server
└── package.json
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Ensure the backend API is running and accessible via Dapr

## Running the Application

### With Dapr

Run the frontend with Dapr sidecar:

```bash
dapr run --app-id frontend --app-port 3000 --dapr-http-port 3500 -- node server.js
```

### Without Dapr (for development)

```bash
npm start
```

The application will be available at `http://localhost:3000`

## Usage

### Regular User Flow

1. Navigate to `http://localhost:3000`
2. Enter any email and password (e.g., `user@example.com`)
3. You'll be redirected to the dashboard where you can:
   - View your appointments
   - Book new appointments
   - Cancel existing appointments

### Admin Flow

1. Navigate to `http://localhost:3000`
2. Login with email: `admin@petclinic.com` (any password)
3. You'll be redirected to the admin panel where you can:
   - Charge appointments by entering the appointment ID

## API Integration

The frontend uses Dapr Client to communicate with the backend API (app-id: `backend`):

### Endpoints Used

- **POST** `/appointment` - Create new appointment
- **GET** `/appointments/email/{owner_email}` - List appointments by email
- **GET** `/appointments/byId/{appointment_id}` - Get specific appointment
- **POST** `/appointment/charge/{appointment_id}` - Charge appointment (admin only)
- **DELETE** `/appointments/{appointment_id}` - Cancel appointment

## Configuration

You can configure the following in `server.js`:

- **PORT**: Application port (default: 3000)
- **Dapr App ID**: Backend service ID (default: 'backend')
- **Dapr Port**: Dapr sidecar port (default: 3500)

## Models

All models are based on the OpenAPI specification:

- **Animal**: Pet information (name, type, breed, age)
- **Owner**: Owner details (name, email, phone)
- **Appointment**: Full appointment details
- **AppointmentCreate**: Data for creating new appointments
- **AppointmentSummary**: Simplified appointment view

## Security Note

⚠️ **This is a demo application** with a fake login system. In production:
- Implement proper authentication
- Add authorization checks
- Validate all inputs
- Use HTTPS
- Secure session configuration
- Add CSRF protection

## Technologies Used

- **Express 5**: Web framework
- **EJS**: Templating engine
- **Dapr Client**: Service invocation
- **Express Session**: Session management
- **Native CSS**: Styling (no external CSS frameworks)
