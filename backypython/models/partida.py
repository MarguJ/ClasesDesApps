from dataclasses import dataclass

from models.equipo import Equipo


@dataclass
class Partida:
    id: int | None
    equipo_local_id: int
    equipo_visitante_id: int
    puntaje_local: int = 0
    puntaje_visitante: int = 0
    fecha_partida: str | None = None
    equipo_local: Equipo | None = None
    equipo_visitante: Equipo | None = None

    def __str__(self) -> str:
        local = self.equipo_local.nombre if self.equipo_local else f"Equipo #{self.equipo_local_id}"
        visitante = self.equipo_visitante.nombre if self.equipo_visitante else f"Equipo #{self.equipo_visitante_id}"
        fecha = self.fecha_partida if self.fecha_partida else "Sin fecha"
        return f"[{self.id}] {local} {self.puntaje_local} - {self.puntaje_visitante} {visitante} | {fecha}"
