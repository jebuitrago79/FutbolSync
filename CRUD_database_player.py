from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Crear valoraciones para un jugador
def create_playerf(playerf_data):
    session = SessionLocal()
    try:
        playerf = PlayerF(**playerf_data)
        session.add(playerf)
        session.commit()
        session.refresh(playerf)
        return playerf
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al crear valoraciones de jugador: {e}")
    finally:
        session.close()

# Leer valoraciones de un jugador por ID
def get_playerf_by_id(playerf_id):
    session = SessionLocal()
    try:
        playerf = session.query(PlayerF).filter(PlayerF.id == playerf_id).first()
        return playerf
    except SQLAlchemyError as e:
        print(f"Error al obtener valoraciones de jugador: {e}")
    finally:
        session.close()

# Leer todas las valoraciones
def get_all_playerf():
    session = SessionLocal()
    try:
        playerfs = session.query(PlayerF).all()
        return playerfs
    except SQLAlchemyError as e:
        print(f"Error al obtener todas las valoraciones de jugadores: {e}")
    finally:
        session.close()

# Actualizar valoraciones de un jugador
def update_playerf(playerf_id, updated_data):
    session = SessionLocal()
    try:
        playerf = session.query(PlayerF).filter(PlayerF.id == playerf_id).first()
        if playerf:
            for key, value in updated_data.items():
                setattr(playerf, key, value)
            session.commit()
            session.refresh(playerf)
            return playerf
        else:
            print(f"Valoraciones del jugador con ID {playerf_id} no encontradas")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al actualizar valoraciones de jugador: {e}")
    finally:
        session.close()

# Eliminar valoraciones de un jugador
def delete_playerf(playerf_id):
    session = SessionLocal()
    try:
        playerf = session.query(PlayerF).filter(PlayerF.id == playerf_id).first()
        if playerf:
            session.delete(playerf)
            session.commit()
            return True
        else:
            print(f"Valoraciones del jugador con ID {playerf_id} no encontradas")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error al eliminar valoraciones de jugador: {e}")
    finally:
        session.close()
