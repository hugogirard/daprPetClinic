from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class AnimalType(str, Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    HAMSTER = "hamster"
    OTHER = "other"


class Animal(BaseModel):
    name: str = Field(..., description="Name of the animal")
    type: AnimalType = Field(..., description="Type of animal")
    breed: Optional[str] = Field(None, description="Breed of the animal")
    age: Optional[int] = Field(None, ge=0, description="Age in years")