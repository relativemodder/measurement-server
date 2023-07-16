from pydantic import BaseModel

class SetSettingModel(BaseModel):
    k: str
    v: str