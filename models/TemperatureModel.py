from pydantic import BaseModel

class TemperatureModel(BaseModel):
    thermometer_id: int
    value: float