from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update, delete
from jugador import *
from player import *
from CRUD_database_player import *
from CRUD_database_player import *

# Crear jugador (asincrónico)
async def new_jugador(jugador_data, session: AsyncSession):
    jugador = Jugador(**jugador_data)
    session.add(jugador)
    await session.commit()
    await session.refresh(jugador)
    return jugador

# Leer todos los jugadores (asincrónico)
async def read_all_players(session: AsyncSession):
    result = await session.execute(select(Jugador))
    return result.scalars().all()

# Leer un jugador por ID (asincrónico)
async def read_one_player(player_id: int, session: AsyncSession):
    result = await session.execute(select(Jugador).filter(Jugador.id == player_id))
    return result.scalar_one_or_none()

# Actualizar jugador (asincrónico)
async def modify_player(player_id: int, updated_data, session: AsyncSession):
    stmt = update(Jugador).where(Jugador.id == player_id).values(updated_data).execution_options(synchronize_session="fetch")
    result = await session.execute(stmt)
    await session.commit()
    return result

# Eliminar jugador (asincrónico)
async def remove_player(player_id: int, session: AsyncSession):
    stmt = delete(Jugador).where(Jugador.id == player_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

# Funciones CRUD para PlayerF (similares)
async def new_playerf(playerf_data, session: AsyncSession):
    playerf = PlayerF(**playerf_data)
    session.add(playerf)
    await session.commit()
    await session.refresh(playerf)
    return playerf

async def read_all_playerf(session: AsyncSession):
    result = await session.execute(select(PlayerF))
    return result.scalars().all()

async def read_one_playerf(playerf_id: int, session: AsyncSession):
    result = await session.execute(select(PlayerF).filter(PlayerF.id == playerf_id))
    return result.scalar_one_or_none()

async def modify_playerf(playerf_id: int, updated_data, session: AsyncSession):
    stmt = update(PlayerF).where(PlayerF.id == playerf_id).values(updated_data).execution_options(synchronize_session="fetch")
    result = await session.execute(stmt)
    await session.commit()
    return result

async def remove_playerf(playerf_id: int, session: AsyncSession):
    stmt = delete(PlayerF).where(PlayerF.id == playerf_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
