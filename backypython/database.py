import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "nexalyst_league.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def inicializar_base_de_datos() -> None:
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS equipos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                patrocinador TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_DATE
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL UNIQUE,
                nombre_real TEXT NOT NULL,
                rol TEXT CHECK(rol IN ('Capitan', 'Jugador', 'Suplente')) NOT NULL,
                equipo_id INTEGER,
                FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE SET NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipo_local_id INTEGER NOT NULL,
                equipo_visitante_id INTEGER NOT NULL,
                puntaje_local INTEGER DEFAULT 0,
                puntaje_visitante INTEGER DEFAULT 0,
                fecha_partida TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (equipo_local_id) REFERENCES equipos(id),
                FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id),
                CHECK (equipo_local_id <> equipo_visitante_id)
            )
            """
        )
        connection.commit()
    finally:
        connection.close()
