from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Appointment(BaseModel):
    id: str = Field(..., description="Unique appointment ID")
    email: str
    animal_name: str = Field(..., description="Name of the animal")
    appointment_date: str = Field(...,alias="appointmentDate")
    reason: str
    notes: Optional[str] = None    
    created_at: str = Field(...,alias="createdAt")

    class Config:
        populate_by_name = True