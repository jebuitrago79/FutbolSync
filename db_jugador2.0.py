import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Crear base declarativa
Base = declarative_base()

# Modelo Jugador (permitir valores NULL en las columnas opcionales)
class Jugador(Base):
    __tablename__ = 'jugadores'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    age = Column(Integer, nullable=True)
    nationality = Column(String(25), nullable=True)
    height = Column(Float, nullable=True)
    team = Column(String(25), nullable=True)
    position = Column(String(100), nullable=True)  # Permite posiciones vacías
    dorsal = Column(Integer, nullable=True)
    goalkeeper = Column(Boolean, nullable=True)

# Modelo PlayerF (permitir valores NULL en las columnas opcionales)
class PlayerF(Base):
    __tablename__ = 'valoraciones'
    id = Column(Integer, primary_key=True)
    overall = Column(Float, nullable=True)
    power_shot = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    passing = Column(Float, nullable=True)
    shooting = Column(Float, nullable=True)
    defending = Column(Float, nullable=True)
    physical = Column(Float, nullable=True)

# Crear motor y base de datos
engine = create_engine("sqlite:///jugadores.db")
Base.metadata.create_all(engine)

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

# Leer CSV
df = pd.read_csv("players_equipos_europeos_22.csv")

# Eliminar solo las filas con datos faltantes en los campos obligatorios, no en todos
df = df.reset_index(drop=True)

# Insertar datos en la tabla Jugador
for _, row in df.iterrows():
    jugador = Jugador(
        id=int(row['sofifa_id']),
        name=row['long_name'],
        age=int(row['age']) if pd.notnull(row['age']) else None,
        nationality=row['nationality_name'] if pd.notnull(row['nationality_name']) else None,
        height=float(row['height_cm']) if pd.notnull(row['height_cm']) else None,
        team=row['club_name'] if pd.notnull(row['club_name']) else None,
        position=row['player_positions'].strip() if pd.notnull(row['player_positions']) else None,
        dorsal=int(row['club_jersey_number']) if pd.notnull(row['club_jersey_number']) else None,
        goalkeeper='GK' in row['player_positions'] if pd.notnull(row['player_positions']) else None
    )
    session.merge(jugador)  # merge permite evitar duplicados por id

# Insertar datos en la tabla PlayerF
for _, row in df.iterrows():
    player = PlayerF(
        id=int(row['sofifa_id']),
        overall=float(row['overall']) if pd.notnull(row['overall']) else None,
        power_shot=float(row['power_shot_power']) if pd.notnull(row['power_shot_power']) else None,
        speed=float(row['pace']) if pd.notnull(row['pace']) else None,
        passing=float(row['passing']) if pd.notnull(row['passing']) else None,
        shooting=float(row['shooting']) if pd.notnull(row['shooting']) else None,
        defending=float(row['defending']) if pd.notnull(row['defending']) else None,
        physical=float(row['physic']) if pd.notnull(row['physic']) else None
    )
    session.merge(player)

# Confirmar cambios
session.commit()
session.close()
print("Base de datos 'jugadores.db' creada y poblada exitosamente.")
