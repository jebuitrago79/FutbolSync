import csv
from typing import Optional
from jugador import Jugador, JugadorwithId


# Asegúrate de que esta ruta sea la misma usada en tu proyecto
JUGADORES_DATABASE_FILENAME = "jugador.csv"

# Los campos que tu app espera (esto debe coincidir con COLUMN_FIELDS)
COLUMN_FIELDS = [
    "id", "name", "age", "nationality", "height", "team", "position",
    "dorsal", "goalkeeper", "goals", "assists", "yellow_cards", "red_cards", "saves"
]


def convert_row(row):
    row["id"] = int(row["id"])
    row["age"] = int(row["age"])
    row["dorsal"] = int(row["dorsal"])
    row["goalkeeper"] = str(row["goalkeeper"]).lower() in ["1", "true"]
    row["goals"] = int(row["goals"])
    row["assists"] = int(row["assists"])
    row["yellow_cards"] = int(row["yellow_cards"])
    row["red_cards"] = int(row["red_cards"])
    row["saves"] = int(row["saves"])

    row["stats"] = {
        "goals": row["goals"],
        "assists": row["assists"],
        "yellow_cards": row["yellow_cards"],
        "red_cards": row["red_cards"],
        "saves": row["saves"],
    }

    return row

def read_all_players():
    with open(JUGADORES_DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        return [JugadorwithId(**convert_row(row)) for row in reader]

def read_one_player(player_id: int):
    with open(JUGADORES_DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["id"]) == player_id:
                return JugadorwithId(**convert_row(row))

def get_next_id():
    try:
        with open(JUGADORES_DATABASE_FILENAME, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            ids = [int(row["id"]) for row in reader if row["id"].isdigit()]
            return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1


def save_player_to_csv(player: JugadorwithId):
    data = player.model_dump()
    if "stats" in data:
        data.update(data.pop("stats"))  # Aplana el dict de stats
    with open(JUGADORES_DATABASE_FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMN_FIELDS)
        writer.writerow(data)


def new_jugador(player: Jugador):
    id: int = get_next_id()
    player_with_id = JugadorwithId(id=id, **player.model_dump())
    save_player_to_csv(player_with_id)
    return player_with_id

def modify_player(id: int, data: dict):
    players = read_all_players()
    updated_player: Optional[JugadorwithId] = None

    for i, p in enumerate(players):
        if p.id == id:

            for field, value in data.items():
                if hasattr(p, field): #verificar
                    setattr(p, field, value) # actualizar
                elif hasattr(p.stats, field):
                    setattr(p.stats, field, value)
            updated_player = players[i]
            break

    if updated_player:
        with open(JUGADORES_DATABASE_FILENAME, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMN_FIELDS)
            writer.writeheader()
            for p in players:
                row_data = p.model_dump()
                row_data.update(row_data.pop("stats"))  # Aplanar stats
                writer.writerow(row_data)
        return updated_player

    return None


def remove_player(id: int):
    players = read_all_players()
    deleted_player: Optional[JugadorwithId] = None

    with open(JUGADORES_DATABASE_FILENAME, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMN_FIELDS)
        writer.writeheader()
        for p in players:
            if p.id == id:
                deleted_player = p
                continue
            row_data = p.model_dump()
            row_data.update(row_data.pop("stats"))  # Aplanar stats
            writer.writerow(row_data)

    return deleted_player