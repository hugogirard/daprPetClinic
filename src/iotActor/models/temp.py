from pydantic import BaseModel

class TempReport(BaseModel):
    indoor_temp: float
    outdoor_temp: float

class TargetTemp(BaseModel):
    target_temp: float