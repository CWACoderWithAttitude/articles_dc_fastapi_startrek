from pydantic import BaseModel

class ShipModel(BaseModel):
    id: int
    name: str
    type: str
    length: float
    width: float
    draft: float

    class Config:
        orm_mode = True