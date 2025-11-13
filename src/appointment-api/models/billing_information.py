from pydantic import BaseModel,Field

class BillingInformation(BaseModel):
    amount: float = Field(...,alias="amount")
    appointment_id: str = Field(...,alias="appointmentId")
    owner_name: str = Field(...,alias="ownerName")
    owner_email: str = Field(..., alias="ownerEmail")
    pet_name: str = Field(..., alias="petName")
    appointment_reason: str = Field(..., alias="appointmentReason")