from dataclasses import dataclass

from models.equipo import Equipo


@dataclass
class Jugador:
    id: int | None
    nickname: str
    nombre_real: str
    rol: str
    equipo_id: int | None = None
    equipo: Equipo | None = None

    def __str__(self) -> str:
        equipo = self.equipo.nombre if self.equipo else "Sin equipo"
        return f"[{self.id}] {self.nickname} ({self.nombre_real}) | {self.rol} | Equipo: {equipo}"
