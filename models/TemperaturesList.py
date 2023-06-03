from pydantic import BaseModel
from typing import Dict, List
from models.TemperatureModel import TemperatureModel
from datetime import datetime

class TemperaturesList:
    temps: Dict[int, List[TemperatureModel]]