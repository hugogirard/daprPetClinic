from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from .animal import Animal
from .owner import Owner


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AppointmentCreate(BaseModel):
    animal: Animal
    owner: Owner
    appointment_date: datetime = Field(..., description="Date and time of appointment")
    reason: str = Field(..., description="Reason for visit")
    notes: Optional[str] = Field(None, description="Additional notes")


class Appointment(BaseModel):
    id: str = Field(..., description="Unique appointment ID")
    animal: Animal
    owner: Owner
    appointment_date: datetime
    reason: str
    notes: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    created_at: datetime
