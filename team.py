from typing import List
from pydantic import BaseModel, Field
from jugador import *

class Team(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    country: str = Field(..., min_length=3, max_length=20)
    players: List[Jugador] = []