from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Definir la sesión
engine = create_engine("sqlite:///jugadores.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear jugador
def create_jugador(jugador_data):
    session = SessionLocal()
    try:
        jugador = Jugador(**jugador_data)
        session.add(jugador)
        session.commit()
        session.refresh(jugador)
        return jugador
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al crear jugador: {e}")
    finally:
        session.close()

# Leer jugador por ID
def get_jugador_by_id(jugador_id):
    session = SessionLocal()
    try:
        jugador = session.query(Jugador).filter(Jugador.id == jugador_id).first()
        return jugador
    except SQLAlchemyError as e:
        print(f"Error al obtener jugador: {e}")
    finally:
        session.close()

# Leer todos los jugadores
def get_all_jugadores():
    session = SessionLocal()
    try:
        jugadores = session.query(Jugador).all()
        return jugadores
    except SQLAlchemyError as e:
        print(f"Error al obtener todos los jugadores: {e}")
    finally:
        session.close()

# Actualizar jugador
def update_jugador(jugador_id, updated_data):
    session = SessionLocal()
    try:
        jugador = session.query(Jugador).filter(Jugador.id == jugador_id).first()
        if jugador:
            for key, value in updated_data.items():
                setattr(jugador, key, value)
            session.commit()
            session.refresh(jugador)
            return jugador
        else:
            print(f"Jugador con ID {jugador_id} no encontrado")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al actualizar jugador: {e}")
    finally:
        session.close()

# Eliminar jugador
def delete_jugador(jugador_id):
    session = SessionLocal()
    try:
        jugador = session.query(Jugador).filter(Jugador.id == jugador_id).first()
        if jugador:
            session.delete(jugador)
            session.commit()
            return True
        else:
            print(f"Jugador con ID {jugador_id} no encontrado")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al eliminar jugador: {e}")
    finally:
        session.close()
