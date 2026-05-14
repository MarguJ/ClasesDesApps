# Nexalyst League Backend

Backend de consola en Python para gestionar equipos, jugadores y partidas de un torneo de esports.

## Ejecutar

```bash
cd backypython
python main.py
```

La base SQLite se crea automaticamente como `nexalyst_league.db`.

## Estructura

- `models/`: entidades del dominio (`Equipo`, `Jugador`, `Partida`).
- `repositories/`: acceso a datos con SQL puro, `sqlite3`, tuplas e indices.
- `database.py`: conexion manual e inicializacion de tablas.
- `main.py`: interfaz de consola con CRUD completo, historial y tabla de posiciones.

## Nota sobre roles

Para evitar problemas de codificacion en consola y SQLite, el rol de capitan se guarda como `Capitan`.
