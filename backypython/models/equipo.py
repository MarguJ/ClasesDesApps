from dataclasses import dataclass


@dataclass
class Equipo:
    id: int | None
    nombre: str
    patrocinador: str | None = None
    fecha_creacion: str | None = None

    def __str__(self) -> str:
        sponsor = self.patrocinador if self.patrocinador else "Sin patrocinador"
        fecha = self.fecha_creacion if self.fecha_creacion else "Sin fecha"
        return f"[{self.id}] {self.nombre} | {sponsor} | Creado: {fecha}"
