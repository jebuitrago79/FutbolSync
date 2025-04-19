from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update, delete
from jugador import Jugador, Estadisticas
import csv

# Leer jugadores desde el CSV y adaptarlos al modelo Jugador
def read_jugadores_from_csv(path="jugador.csv"):
    jugadores = []
    with open(path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            try:
                stats = Estadisticas(
                    goals=int(row.get("goals", 0) or 0),
                    assists=int(row.get("assists", 0) or 0),
                    yellow_cards=int(row.get("yellow_cards", 0) or 0),
                    red_cards=int(row.get("red_cards", 0) or 0),
                    saved=int(row.get("saved", 0) or 0),
                    conceded=int(row.get("conceded", 0) or 0),
                )
                jugador = Jugador(
                    id=int(row.get("id", idx)),
                    name=row["name"],
                    age=int(row["age"]),
                    nationality=row["nationality"],
                    height=float(row["height"]),
                    team=row["team"],
                    position=row["position"],
                    dorsal=int(row["dorsal"]),
                    goalkeeper="GK" in row["position"].upper(),
                    stats=stats
                )
                jugadores.append(jugador)
            except Exception as e:
                print(f"Error al procesar jugador en fila {idx}: {e}")
    return jugadores

# Crear jugador
async def new_jugador(jugador_data, session: AsyncSession):
    jugador = Jugador(**jugador_data)
    session.add(jugador)
    await session.commit()
    await session.refresh(jugador)
    return jugador

# Leer todos los jugadores
async def read_all_players(session: AsyncSession):
    result = await session.execute(select(Jugador))
    return result.scalars().all()

# Leer un jugador por ID
async def read_one_player(player_id: int, session: AsyncSession):
    result = await session.execute(select(Jugador).filter(Jugador.id == player_id))
    return result.scalar_one_or_none()

# Actualizar jugador
async def modify_player(player_id: int, updated_data, session: AsyncSession):
    stmt = update(Jugador).where(Jugador.id == player_id).values(updated_data).execution_options(synchronize_session="fetch")
    await session.execute(stmt)
    await session.commit()
    return await read_one_player(player_id, session)

# Eliminar jugador
async def delete_player(player_id: int, session: AsyncSession):
    stmt = delete(Jugador).where(Jugador.id == player_id)
    await session.execute(stmt)
    await session.commit()
    return {"message": f"Jugador {player_id} eliminado correctamente"}

# ⚙️ Configuración de la base de datos
DATABASE_URL = "sqlite+aiosqlite:///./jugadores.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependencia para FastAPI
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session