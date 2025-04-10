from dataclasses import Field

from pydantic import BaseModel,Field
from jugador import *
class playerF(BaseModel):
#Estadsiticas de valoracion efootball
    overall:float
    power_shot:float
    speed:float
    passing:float
    shooting:float
    defending:float
    physical:float

