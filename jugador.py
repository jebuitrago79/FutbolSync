from dataclasses import Field
from typing import Optional
from pydantic import BaseModel,Field

class estadisticas(BaseModel):
    # Estadisticas vida real
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int

    #para arquero
    saved: int
    conceded : int

class Jugador(BaseModel):
    name: str = Field(..., min_length=2, max_length=40)
    age: int
    nationality: str = Field(..., min_length=2, max_length=25)
    height : float
    team:str=Field(...,min_length=2, max_length=25)
    position: str = Field(..., min_length=2, max_length=25)
    dorsal: int = Field(..., ge=1, le=99)
    goalkeeper : bool
    stats: estadisticas



class JugadorwithId(Jhugador):
        id: int