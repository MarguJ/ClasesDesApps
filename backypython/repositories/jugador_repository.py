from database import get_connection
from models.jugador import Jugador
from repositories.equipo_repository import EquipoRepository


class JugadorRepository:
    def __init__(self) -> None:
        self.equipo_repository = EquipoRepository()

    def crear(self, jugador: Jugador) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO jugadores (nickname, nombre_real, rol, equipo_id) VALUES (?, ?, ?, ?)",
                (jugador.nickname, jugador.nombre_real, jugador.rol, jugador.equipo_id),
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def obtener_todos(self) -> list[Jugador]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, nickname, nombre_real, rol, equipo_id FROM jugadores")
            filas = cursor.fetchall()
            return [self._mapear_jugador(fila) for fila in filas]
        finally:
            connection.close()

    def obtener_por_id(self, jugador_id: int) -> Jugador | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, nickname, nombre_real, rol, equipo_id FROM jugadores WHERE id = ?",
                (jugador_id,),
            )
            fila = cursor.fetchone()
            return self._mapear_jugador(fila) if fila else None
        finally:
            connection.close()

    def obtener_por_equipo(self, equipo_id: int) -> list[Jugador]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, nickname, nombre_real, rol, equipo_id FROM jugadores WHERE equipo_id = ?",
                (equipo_id,),
            )
            filas = cursor.fetchall()
            return [self._mapear_jugador(fila) for fila in filas]
        finally:
            connection.close()

    def actualizar(self, jugador: Jugador) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE jugadores SET nickname = ?, nombre_real = ?, rol = ?, equipo_id = ? WHERE id = ?",
                (jugador.nickname, jugador.nombre_real, jugador.rol, jugador.equipo_id, jugador.id),
            )
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def eliminar(self, jugador_id: int) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM jugadores WHERE id = ?", (jugador_id,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def _mapear_jugador(self, fila: tuple) -> Jugador:
        equipo_id = fila[4]
        equipo = self.equipo_repository.obtener_por_id(equipo_id) if equipo_id else None
        return Jugador(
            id=fila[0],
            nickname=fila[1],
            nombre_real=fila[2],
            rol=fila[3],
            equipo_id=equipo_id,
            equipo=equipo,
        )
