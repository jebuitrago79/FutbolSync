from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from jugador import *
from player import *
from operations_database import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HOLA PROYECTO FutbolSync!"}


async def cargar_jugadores():
    jugadores = read_jugadores_from_csv()
    async with AsyncSessionLocal() as session:
        for jugador in jugadores:
            try:
                await new_jugador(jugador.dict(), session)
            except Exception as e:
                print(f"NO SE PUDO INSERTAR{jugador.name}:{e}")

# Endpoint: Crear un nuevo jugador
@app.post("/jugadores/", response_model=Jugador)
def create_jugador(jugador: Jugador):
    try:
        jugador_db = create_jugador(jugador.dict())
        return jugador_db
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el jugador")

# Endpoint: Obtener todos los jugadores
@app.get("/jugadores")
async def get_all_jugadores(session: AsyncSession = Depends(get_async_session)):
    jugadores = await read_all_players(session)
    return jugadores

# Endpoint: Obtener un jugador por su ID
@app.get("/jugadores/{jugador_id}", response_model=Jugador)
def get_jugador(jugador_id: int):
    jugador = get_jugador_by_id(jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

# Endpoint: Actualizar un jugador por su ID
@app.put("/jugadores/{jugador_id}", response_model=Jugador)
def update_jugador(jugador_id: int, updated_data: Jugador):
    updated_jugador = update_jugador(jugador_id, updated_data.dict())
    if not updated_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return updated_jugador

# Endpoint: Eliminar un jugador por su ID
@app.delete("/jugadores/{jugador_id}")
def delete_jugador(jugador_id: int):
    result = delete_jugador(jugador_id)
    if not result:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador eliminado correctamente"}


# Endpoint: Crear una valoración de jugador
@app.post("/playerf/", response_model=PlayerF)
def create_playerf(playerf: PlayerF):
    try:
        playerf_db = create_playerf(playerf.dict())
        return playerf_db
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear la valoración del jugador")

# Endpoint: Obtener todas las valoraciones de jugadores
@app.get("/playerf/", response_model=List[PlayerF])
def get_all_playerf():
    playerfs = get_all_playerf()
    if not playerfs:
        raise HTTPException(status_code=404, detail="No valoraciones encontradas")
    return playerfs

# Endpoint: Obtener una valoración de jugador por su ID
@app.get("/playerf/{playerf_id}", response_model=PlayerF)
def get_playerf(playerf_id: int):
    playerf = get_playerf_by_id(playerf_id)
    if not playerf:
        raise HTTPException(status_code=404, detail="Valoración de jugador no encontrada")
    return playerf

# Endpoint: Actualizar una valoración de jugador por su ID
@app.put("/playerf/{playerf_id}", response_model=PlayerF)
def update_playerf(playerf_id: int, updated_data: PlayerF):
    updated_playerf = update_playerf(playerf_id, updated_data.dict())
    if not updated_playerf:
        raise HTTPException(status_code=404, detail="Valoración de jugador no encontrada")
    return updated_playerf

# Endpoint: Eliminar una valoración de jugador por su ID
@app.delete("/playerf/{playerf_id}")
def delete_playerf(playerf_id: int):
    result = delete_playerf(playerf_id)
    if not result:
        raise HTTPException(status_code=404, detail="Valoración de jugador no encontrada")
    return {"message": "Valoración de jugador eliminada correctamente"}

