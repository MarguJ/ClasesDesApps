from database import get_connection
from models.equipo import Equipo


class EquipoRepository:
    def crear(self, equipo: Equipo) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO equipos (nombre, patrocinador) VALUES (?, ?)",
                (equipo.nombre, equipo.patrocinador),
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def obtener_todos(self) -> list[Equipo]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, nombre, patrocinador, fecha_creacion FROM equipos")
            filas = cursor.fetchall()
            return [self._mapear_equipo(fila) for fila in filas]
        finally:
            connection.close()

    def obtener_por_id(self, equipo_id: int) -> Equipo | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, nombre, patrocinador, fecha_creacion FROM equipos WHERE id = ?",
                (equipo_id,),
            )
            fila = cursor.fetchone()
            return self._mapear_equipo(fila) if fila else None
        finally:
            connection.close()

    def actualizar(self, equipo: Equipo) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE equipos SET nombre = ?, patrocinador = ? WHERE id = ?",
                (equipo.nombre, equipo.patrocinador, equipo.id),
            )
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def eliminar(self, equipo_id: int) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM equipos WHERE id = ?", (equipo_id,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def _mapear_equipo(self, fila: tuple) -> Equipo:
        return Equipo(
            id=fila[0],
            nombre=fila[1],
            patrocinador=fila[2],
            fecha_creacion=fila[3],
        )
