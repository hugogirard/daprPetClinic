from pydantic import BaseModel, Field


class Owner(BaseModel):
    name: str = Field(..., description="Owner's full name")
    email: str = Field(..., description="Owner's email")
    phone: str = Field(..., description="Owner's phone number")
