from pydantic import BaseModel

class PlayerF(BaseModel):
    id: int
    name: str
    age: int
    nationality: str
    team: str
    position: str

    class Config:
        from_attributes = True  # Asegúrate de usar 'from_attributes' en vez de 'orm_mode'