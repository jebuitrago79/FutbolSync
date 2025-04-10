from fastapi import FastAPI, HTTPException
from typing import List
from jugador import *
from operations_jugador import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the FIFA/Champions Players API"}


@app.post("/players", response_model=JugadorwithId)
async def create_player(j: Jugador):
    return new_jugador(j)


@app.get("/players", response_model=List[JugadorwithId])
async def list_players():
    return read_all_players()


@app.get("/players/{player_id}", response_model=JugadorwithId)
async def get_player(player_id: int):
    player = read_one_player(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.put("/players/{player_id}", response_model=JugadorwithId)
async def update_player(player_id: int, data: Jugador):
    player = modify_player(player_id, data.model_dump())
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.delete("/players/{player_id}", response_model=JugadorwithId)
async def delete_player(player_id: int):
    player = remove_player(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
