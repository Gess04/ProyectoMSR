"""
utils.py
==========
Funciones auxiliares de formato, validación y presentación. Se separan del
resto del proyecto para no mezclar la lógica del grafo o de Dijkstra con la
lógica de interacción con el usuario.
"""

import config


def nombre_vertice(vertice):
    """Convierte una tupla (calle, carrera) en un texto legible, respetando
    la nomenclatura vial de Bogotá."""
    calle, carrera = vertice
    return f"Calle {calle} con Carrera {carrera}"


def _normalizar(texto):
    return texto.strip().lower()


def buscar_establecimiento(nombre):
    """Busca un establecimiento en config.ESTABLECIMIENTOS sin importar
    mayúsculas/minúsculas ni espacios extra. Retorna la tupla
    (calle, carrera) o None si no existe."""
    nombre = _normalizar(nombre)
    for clave, vertice in config.ESTABLECIMIENTOS.items():
        if _normalizar(clave) == nombre:
            return vertice
    return None


def listar_establecimientos():
    return list(config.ESTABLECIMIENTOS.keys())


def imprimir_camino(nombre_persona, camino, costo):
    print(f"\nRuta de {nombre_persona} (tiempo total: {costo} minutos):")
    for vertice in camino:
        print(f"  -> {nombre_vertice(vertice)}")
