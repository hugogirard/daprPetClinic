from fastapi import HTTPException
from fastapi import APIRouter
from typing import Optional, List
from models import Appointment, AppointmentCreate, AppointmentSummary
from services import AppointmentService

appointment_service = AppointmentService()
router = APIRouter()

@router.post("/appointment", response_model=Appointment, status_code=201)
def create_appointment(appointment_data: AppointmentCreate):
    """Create a new appointment for a pet"""
    return appointment_service.create_appointment(appointment_data)


@router.get("/appointments/email/{owner_email}", response_model=List[AppointmentSummary])
def list_appointments(owner_email:str):
    return appointment_service.get_appointments(owner_email)


@router.get("/appointments/byId/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: str):
    """Get a specific appointment by ID"""
    appointment = appointment_service.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.post("/appointment/charge/{appointment_id}", status_code=202)
def charge_appointment(appointment_id: str):
    """Update the status of an appointment"""
    appointment_service.charge_appointment(appointment_id)
    return {}, 202


@router.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: str):
    """Cancel and delete an appointment"""
    if not appointment_service.cancel_appointment(appointment_id):
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": f"Appointment {appointment_id} has been cancelled"}