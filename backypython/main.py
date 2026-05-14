import sqlite3

from database import DB_PATH, inicializar_base_de_datos
from models.equipo import Equipo
from models.jugador import Jugador
from models.partida import Partida
from repositories.equipo_repository import EquipoRepository
from repositories.jugador_repository import JugadorRepository
from repositories.partida_repository import PartidaRepository


ROLES_VALIDOS = ("Capitan", "Jugador", "Suplente")


def leer_texto(mensaje: str, obligatorio: bool = True) -> str | None:
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor if valor else None
        print("El valor es obligatorio.")


def leer_entero(mensaje: str, obligatorio: bool = True) -> int | None:
    while True:
        valor = input(mensaje).strip()
        if not valor and not obligatorio:
            return None
        try:
            return int(valor)
        except ValueError:
            print("Ingrese un numero entero valido.")


def leer_rol() -> str:
    while True:
        rol = leer_texto("Rol (Capitan/Jugador/Suplente): ")
        if rol in ROLES_VALIDOS:
            return rol
        print("Rol invalido. Opciones disponibles: Capitan, Jugador, Suplente.")


def pausar() -> None:
    input("\nPresione Enter para continuar...")


def imprimir_titulo(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def mostrar_equipos(equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("EQUIPOS")
    equipos = equipo_repo.obtener_todos()
    if not equipos:
        print("No hay equipos registrados.")
        return
    for equipo in equipos:
        print(equipo)


def crear_equipo(equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("CREAR EQUIPO")
    nombre = leer_texto("Nombre: ")
    patrocinador = leer_texto("Patrocinador (opcional): ", obligatorio=False)
    equipo_id = equipo_repo.crear(Equipo(id=None, nombre=nombre, patrocinador=patrocinador))
    print(f"Equipo creado con ID {equipo_id}.")


def actualizar_equipo(equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("ACTUALIZAR EQUIPO")
    mostrar_equipos(equipo_repo)
    equipo_id = leer_entero("ID del equipo: ")
    equipo = equipo_repo.obtener_por_id(equipo_id)
    if not equipo:
        print("No existe un equipo con ese ID.")
        return

    nombre = leer_texto(f"Nombre [{equipo.nombre}]: ", obligatorio=False) or equipo.nombre
    patrocinador_actual = equipo.patrocinador or ""
    patrocinador = leer_texto(f"Patrocinador [{patrocinador_actual}]: ", obligatorio=False)
    if patrocinador is None:
        patrocinador = equipo.patrocinador

    actualizado = equipo_repo.actualizar(Equipo(equipo_id, nombre, patrocinador, equipo.fecha_creacion))
    print("Equipo actualizado." if actualizado else "No se pudo actualizar el equipo.")


def eliminar_equipo(equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("ELIMINAR EQUIPO")
    mostrar_equipos(equipo_repo)
    equipo_id = leer_entero("ID del equipo: ")
    eliminado = equipo_repo.eliminar(equipo_id)
    print("Equipo eliminado." if eliminado else "No existe un equipo con ese ID.")


def menu_equipos(equipo_repo: EquipoRepository) -> None:
    while True:
        imprimir_titulo("CRUD EQUIPOS")
        print("1. Crear equipo")
        print("2. Listar equipos")
        print("3. Buscar equipo por ID")
        print("4. Actualizar equipo")
        print("5. Eliminar equipo")
        print("0. Volver")
        opcion = input("Opcion: ").strip()

        try:
            if opcion == "1":
                crear_equipo(equipo_repo)
            elif opcion == "2":
                mostrar_equipos(equipo_repo)
            elif opcion == "3":
                equipo = equipo_repo.obtener_por_id(leer_entero("ID del equipo: "))
                print(equipo if equipo else "Equipo no encontrado.")
            elif opcion == "4":
                actualizar_equipo(equipo_repo)
            elif opcion == "5":
                eliminar_equipo(equipo_repo)
            elif opcion == "0":
                return
            else:
                print("Opcion invalida.")
        except sqlite3.Error as error:
            print(f"Error de base de datos: {error}")
        pausar()


def mostrar_jugadores(jugador_repo: JugadorRepository) -> None:
    imprimir_titulo("JUGADORES")
    jugadores = jugador_repo.obtener_todos()
    if not jugadores:
        print("No hay jugadores registrados.")
        return
    for jugador in jugadores:
        print(jugador)


def crear_jugador(jugador_repo: JugadorRepository, equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("CREAR JUGADOR")
    mostrar_equipos(equipo_repo)
    nickname = leer_texto("Nickname: ")
    nombre_real = leer_texto("Nombre real: ")
    rol = leer_rol()
    equipo_id = leer_entero("ID del equipo (opcional): ", obligatorio=False)
    jugador_id = jugador_repo.crear(Jugador(None, nickname, nombre_real, rol, equipo_id))
    print(f"Jugador creado con ID {jugador_id}.")


def actualizar_jugador(jugador_repo: JugadorRepository, equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("ACTUALIZAR JUGADOR")
    mostrar_jugadores(jugador_repo)
    jugador_id = leer_entero("ID del jugador: ")
    jugador = jugador_repo.obtener_por_id(jugador_id)
    if not jugador:
        print("No existe un jugador con ese ID.")
        return

    mostrar_equipos(equipo_repo)
    nickname = leer_texto(f"Nickname [{jugador.nickname}]: ", obligatorio=False) or jugador.nickname
    nombre_real = leer_texto(f"Nombre real [{jugador.nombre_real}]: ", obligatorio=False) or jugador.nombre_real
    print(f"Rol actual: {jugador.rol}")
    rol = leer_texto("Nuevo rol (Enter para mantener): ", obligatorio=False) or jugador.rol
    if rol not in ROLES_VALIDOS:
        print("Rol invalido. No se actualizo el jugador.")
        return
    equipo_id = leer_entero("ID del equipo (Enter para dejar igual): ", obligatorio=False)
    if equipo_id is None:
        equipo_id = jugador.equipo_id

    actualizado = jugador_repo.actualizar(Jugador(jugador_id, nickname, nombre_real, rol, equipo_id))
    print("Jugador actualizado." if actualizado else "No se pudo actualizar el jugador.")


def eliminar_jugador(jugador_repo: JugadorRepository) -> None:
    imprimir_titulo("ELIMINAR JUGADOR")
    mostrar_jugadores(jugador_repo)
    jugador_id = leer_entero("ID del jugador: ")
    eliminado = jugador_repo.eliminar(jugador_id)
    print("Jugador eliminado." if eliminado else "No existe un jugador con ese ID.")


def listar_jugadores_por_equipo(jugador_repo: JugadorRepository, equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("JUGADORES POR EQUIPO")
    mostrar_equipos(equipo_repo)
    equipo_id = leer_entero("ID del equipo: ")
    jugadores = jugador_repo.obtener_por_equipo(equipo_id)
    if not jugadores:
        print("No hay jugadores registrados para ese equipo.")
        return
    for jugador in jugadores:
        print(jugador)


def menu_jugadores(jugador_repo: JugadorRepository, equipo_repo: EquipoRepository) -> None:
    while True:
        imprimir_titulo("CRUD JUGADORES")
        print("1. Crear jugador")
        print("2. Listar jugadores")
        print("3. Buscar jugador por ID")
        print("4. Listar jugadores por equipo")
        print("5. Actualizar jugador")
        print("6. Eliminar jugador")
        print("0. Volver")
        opcion = input("Opcion: ").strip()

        try:
            if opcion == "1":
                crear_jugador(jugador_repo, equipo_repo)
            elif opcion == "2":
                mostrar_jugadores(jugador_repo)
            elif opcion == "3":
                jugador = jugador_repo.obtener_por_id(leer_entero("ID del jugador: "))
                print(jugador if jugador else "Jugador no encontrado.")
            elif opcion == "4":
                listar_jugadores_por_equipo(jugador_repo, equipo_repo)
            elif opcion == "5":
                actualizar_jugador(jugador_repo, equipo_repo)
            elif opcion == "6":
                eliminar_jugador(jugador_repo)
            elif opcion == "0":
                return
            else:
                print("Opcion invalida.")
        except sqlite3.Error as error:
            print(f"Error de base de datos: {error}")
        pausar()


def mostrar_partidas(partida_repo: PartidaRepository) -> None:
    imprimir_titulo("PARTIDAS")
    partidas = partida_repo.historial_con_nombres()
    if not partidas:
        print("No hay partidas registradas.")
        return
    for partida in partidas:
        print(partida)


def crear_partida(partida_repo: PartidaRepository, equipo_repo: EquipoRepository) -> None:
    imprimir_titulo("CREAR PARTIDA")
    mostrar_equipos(equipo_repo)
    equipo_local_id = leer_entero("ID equipo local: ")
    equipo_visitante_id = leer_entero("ID equipo visitante: ")
    puntaje_local = leer_entero("Puntaje local: ")
    puntaje_visitante = leer_entero("Puntaje visitante: ")
    partida_id = partida_repo.crear(
        Partida(None, equipo_local_id, equipo_visitante_id, puntaje_local, puntaje_visitante)
    )
    print(f"Partida creada con ID {partida_id}.")


def actualizar_partida(partida_repo: PartidaRepository) -> None:
    imprimir_titulo("ACTUALIZAR PUNTAJE")
    mostrar_partidas(partida_repo)
    partida_id = leer_entero("ID de la partida: ")
    puntaje_local = leer_entero("Nuevo puntaje local: ")
    puntaje_visitante = leer_entero("Nuevo puntaje visitante: ")
    actualizado = partida_repo.actualizar_puntaje(partida_id, puntaje_local, puntaje_visitante)
    print("Puntaje actualizado." if actualizado else "No existe una partida con ese ID.")


def eliminar_partida(partida_repo: PartidaRepository) -> None:
    imprimir_titulo("ELIMINAR PARTIDA")
    mostrar_partidas(partida_repo)
    partida_id = leer_entero("ID de la partida: ")
    eliminado = partida_repo.eliminar(partida_id)
    print("Partida eliminada." if eliminado else "No existe una partida con ese ID.")


def menu_partidas(partida_repo: PartidaRepository, equipo_repo: EquipoRepository) -> None:
    while True:
        imprimir_titulo("CRUD PARTIDAS")
        print("1. Crear partida")
        print("2. Listar partidas")
        print("3. Buscar partida por ID")
        print("4. Actualizar puntaje")
        print("5. Eliminar partida")
        print("0. Volver")
        opcion = input("Opcion: ").strip()

        try:
            if opcion == "1":
                crear_partida(partida_repo, equipo_repo)
            elif opcion == "2":
                mostrar_partidas(partida_repo)
            elif opcion == "3":
                partida = partida_repo.obtener_por_id(leer_entero("ID de la partida: "))
                print(partida if partida else "Partida no encontrada.")
            elif opcion == "4":
                actualizar_partida(partida_repo)
            elif opcion == "5":
                eliminar_partida(partida_repo)
            elif opcion == "0":
                return
            else:
                print("Opcion invalida.")
        except sqlite3.Error as error:
            print(f"Error de base de datos: {error}")
        pausar()


def mostrar_tabla_posiciones(partida_repo: PartidaRepository) -> None:
    imprimir_titulo("TABLA DE POSICIONES")
    posiciones = partida_repo.tabla_posiciones()
    if not posiciones:
        print("No hay equipos registrados.")
        return

    print(f"{'Equipo':<24} {'PJ':>3} {'PG':>3} {'PE':>3} {'PP':>3} {'GF':>3} {'GC':>3} {'DG':>4} {'PTS':>4}")
    print("-" * 70)
    for fila in posiciones:
        print(
            f"{fila['equipo']:<24} {fila['pj']:>3} {fila['pg']:>3} {fila['pe']:>3} "
            f"{fila['pp']:>3} {fila['gf']:>3} {fila['gc']:>3} {fila['dg']:>4} {fila['pts']:>4}"
        )


def menu_principal() -> None:
    inicializar_base_de_datos()
    equipo_repo = EquipoRepository()
    jugador_repo = JugadorRepository()
    partida_repo = PartidaRepository()

    while True:
        imprimir_titulo("NEXALYST LEAGUE")
        print(f"Base de datos: {DB_PATH}")
        print("1. Gestionar equipos")
        print("2. Gestionar jugadores")
        print("3. Gestionar partidas")
        print("4. Ver historial del torneo")
        print("5. Ver tabla de posiciones")
        print("0. Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            menu_equipos(equipo_repo)
        elif opcion == "2":
            menu_jugadores(jugador_repo, equipo_repo)
        elif opcion == "3":
            menu_partidas(partida_repo, equipo_repo)
        elif opcion == "4":
            mostrar_partidas(partida_repo)
            pausar()
        elif opcion == "5":
            mostrar_tabla_posiciones(partida_repo)
            pausar()
        elif opcion == "0":
            print("Hasta luego.")
            return
        else:
            print("Opcion invalida.")
            pausar()


if __name__ == "__main__":
    menu_principal()
