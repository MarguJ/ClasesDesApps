from database import get_connection
from models.partida import Partida
from repositories.equipo_repository import EquipoRepository


class PartidaRepository:
    def __init__(self) -> None:
        self.equipo_repository = EquipoRepository()

    def crear(self, partida: Partida) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO partidas (
                    equipo_local_id,
                    equipo_visitante_id,
                    puntaje_local,
                    puntaje_visitante
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    partida.equipo_local_id,
                    partida.equipo_visitante_id,
                    partida.puntaje_local,
                    partida.puntaje_visitante,
                ),
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def obtener_todas(self) -> list[Partida]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, equipo_local_id, equipo_visitante_id, puntaje_local, puntaje_visitante, fecha_partida
                FROM partidas
                """
            )
            filas = cursor.fetchall()
            return [self._mapear_partida(fila) for fila in filas]
        finally:
            connection.close()

    def obtener_por_id(self, partida_id: int) -> Partida | None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, equipo_local_id, equipo_visitante_id, puntaje_local, puntaje_visitante, fecha_partida
                FROM partidas
                WHERE id = ?
                """,
                (partida_id,),
            )
            fila = cursor.fetchone()
            return self._mapear_partida(fila) if fila else None
        finally:
            connection.close()

    def actualizar_puntaje(self, partida_id: int, puntaje_local: int, puntaje_visitante: int) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE partidas SET puntaje_local = ?, puntaje_visitante = ? WHERE id = ?",
                (puntaje_local, puntaje_visitante, partida_id),
            )
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def eliminar(self, partida_id: int) -> bool:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM partidas WHERE id = ?", (partida_id,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def historial_con_nombres(self) -> list[Partida]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    p.id,
                    p.equipo_local_id,
                    p.equipo_visitante_id,
                    p.puntaje_local,
                    p.puntaje_visitante,
                    p.fecha_partida,
                    el.nombre,
                    ev.nombre
                FROM partidas p
                JOIN equipos el ON p.equipo_local_id = el.id
                JOIN equipos ev ON p.equipo_visitante_id = ev.id
                """
            )
            filas = cursor.fetchall()
            partidas = []
            for fila in filas:
                partida = self._mapear_partida(fila[:6])
                if partida.equipo_local:
                    partida.equipo_local.nombre = fila[6]
                if partida.equipo_visitante:
                    partida.equipo_visitante.nombre = fila[7]
                partidas.append(partida)
            return partidas
        finally:
            connection.close()

    def tabla_posiciones(self) -> list[dict]:
        equipos = self.equipo_repository.obtener_todos()
        posiciones = {
            equipo.id: {
                "equipo": equipo.nombre,
                "pj": 0,
                "pg": 0,
                "pe": 0,
                "pp": 0,
                "gf": 0,
                "gc": 0,
                "dg": 0,
                "pts": 0,
            }
            for equipo in equipos
        }

        for partida in self.obtener_todas():
            local = posiciones.get(partida.equipo_local_id)
            visitante = posiciones.get(partida.equipo_visitante_id)
            if not local or not visitante:
                continue

            local["pj"] += 1
            visitante["pj"] += 1
            local["gf"] += partida.puntaje_local
            local["gc"] += partida.puntaje_visitante
            visitante["gf"] += partida.puntaje_visitante
            visitante["gc"] += partida.puntaje_local

            if partida.puntaje_local > partida.puntaje_visitante:
                local["pg"] += 1
                local["pts"] += 3
                visitante["pp"] += 1
            elif partida.puntaje_local < partida.puntaje_visitante:
                visitante["pg"] += 1
                visitante["pts"] += 3
                local["pp"] += 1
            else:
                local["pe"] += 1
                visitante["pe"] += 1
                local["pts"] += 1
                visitante["pts"] += 1

        for fila in posiciones.values():
            fila["dg"] = fila["gf"] - fila["gc"]

        return sorted(posiciones.values(), key=lambda item: (item["pts"], item["dg"], item["gf"]), reverse=True)

    def _mapear_partida(self, fila: tuple) -> Partida:
        equipo_local = self.equipo_repository.obtener_por_id(fila[1])
        equipo_visitante = self.equipo_repository.obtener_por_id(fila[2])
        return Partida(
            id=fila[0],
            equipo_local_id=fila[1],
            equipo_visitante_id=fila[2],
            puntaje_local=fila[3],
            puntaje_visitante=fila[4],
            fecha_partida=fila[5],
            equipo_local=equipo_local,
            equipo_visitante=equipo_visitante,
        )
