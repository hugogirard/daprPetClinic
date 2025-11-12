from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from typing import Optional, List
from models import Appointment, AppointmentCreate, AppointmentStatus
from services import AppointmentService

app = FastAPI(title="Pet Clinic Appointment API")
appointment_service = AppointmentService()

@app.post("/appointments", response_model=Appointment, status_code=201)
def create_appointment(appointment_data: AppointmentCreate):
    """Create a new appointment for a pet"""
    return appointment_service.create_appointment(appointment_data)


@app.get("/appointments", response_model=List[Appointment])
def list_appointments(status: Optional[AppointmentStatus] = None):
    """List all appointments, optionally filtered by status"""
    return appointment_service.list_appointments(status)


@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: str):
    """Get a specific appointment by ID"""
    appointment = appointment_service.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@app.put("/appointments/{appointment_id}/status", response_model=Appointment)
def update_appointment_status(appointment_id: str, status: AppointmentStatus):
    """Update the status of an appointment"""
    appointment = appointment_service.update_appointment_status(appointment_id, status)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: str):
    """Cancel and delete an appointment"""
    if not appointment_service.cancel_appointment(appointment_id):
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": f"Appointment {appointment_id} has been cancelled"}

@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")