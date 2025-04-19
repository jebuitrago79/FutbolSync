from typing import Optional
from pydantic import BaseModel, Field

# Modelo para las estadísticas del jugador (vida real y para arquero)
class Estadisticas(BaseModel):
    goals: int = Field(..., ge=0)  # Goles (debe ser >= 0)
    assists: int = Field(..., ge=0)  # Asistencias (debe ser >= 0)
    yellow_cards: int = Field(..., ge=0)  # Tarjetas amarillas (debe ser >= 0)
    red_cards: int = Field(..., ge=0)  # Tarjetas rojas (debe ser >= 0)
    # Estadísticas de arquero
    saved: int = Field(..., ge=0)  # Goles salvados (debe ser >= 0)
    conceded: int = Field(..., ge=0)  # Goles concedidos (debe ser >= 0)

# Modelo Jugador con estadísticas
class Jugador(BaseModel):
    id: int  # 'id' debe ser de tipo int para que Pydantic no genere error
    name: str = Field(..., min_length=2, max_length=40)  # Nombre del jugador
    age: int = Field(..., ge=16)  # Edad (mayor o igual a 16)
    nationality: str = Field(..., min_length=2, max_length=25)  # Nacionalidad
    height: float = Field(..., gt=0)  # Altura (debe ser mayor a 0)
    team: str = Field(..., min_length=2, max_length=25)  # Nombre del equipo
    position: str = Field(..., min_length=2, max_length=25)  # Posición del jugador
    dorsal: int = Field(..., ge=1, le=99)  # Dorsal (entre 1 y 99)
    goalkeeper: bool  # ¿Es arquero?
    stats: Estadisticas  # Estadísticas del jugador

    class Config:
        orm_mode = True  # Permite la conversión de modelos ORM (de base de datos) a Pydantic

# Modelo Jugador con ID para respuesta
class JugadorwithId(Jugador):
    pass  # No es necesario modificar nada aquí