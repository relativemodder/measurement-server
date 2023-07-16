from pydantic import BaseModel
from typing import List
from models.TemperatureModel import TemperatureModel

class TemperaturePostModel(BaseModel):
    temperatures: List[TemperatureModel]
    pseudo_table_id: str