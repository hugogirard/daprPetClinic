from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from .animal import Animal
from .owner import Owner

class AppointmentSummary(BaseModel):
    id: str
    appointment_date: datetime = Field(...,alias="appointmentDate")

    class Config:
      populate_by_name = True

class AppointmentCreate(BaseModel):
    animal: Animal
    owner: Owner
    appointment_date: datetime = Field(..., description="Date and time of appointment",alias="appointmentDate")
    reason: str = Field(..., description="Reason for visit")
    notes: Optional[str] = Field(None, description="Additional notes")


class Appointment(BaseModel):
    id: str = Field(..., description="Unique appointment ID")
    animal: Animal
    owner: Owner
    appointment_date: datetime = Field(...,alias="appointmentDate")
    reason: str
    notes: Optional[str] = None    
    created_at: datetime = Field(...,alias="createdAt")

    class Config:
        populate_by_name = True