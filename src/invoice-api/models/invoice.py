from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


{
    "amount": 250.00,
    "ownerName": "67890",
    "ownerEmail": "67890",
    "petName": "Mozart",
    "appointmentReason": "Annual Vaccine"
}

class InvoiceDetail(BaseModel):
    amount: float
    appointment_id:str
    owner_name:str
    owner_email:str
    pet_name:str
    appointment_reason:str

class Invoice(BaseModel):
    id: str = Field(..., description="Unique invoice ID")
    appointment_id: str = Field(...,alias="appointmentId")
    owner_name: str = Field(...,alias="ownerName")
    owner_email: str = Field(...,alias="ownerEmail")
    animal_name: str = Field(...,alias="animalName")
    issue_date: datetime = Field(...,alias="issueDate")
    due_date: datetime = Field(...,alias="dueDate")
    subtotal: float = Field(...,alias="subTotal")
    tax: float
    total: float
    status:str = "Pending"