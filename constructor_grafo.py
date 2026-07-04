"""
constructor_grafo.py
=======================
Construye el grafo que representa la cuadrícula de calles y carreras
descrita en el enunciado, a partir de los datos declarados en config.py.
No hay ningún número ni dirección "quemado" aquí: los límites de la
cuadrícula y los costos especiales siempre se leen desde config.py, por lo
que basta con editar ese archivo (por ejemplo, para ampliar la zona o
cambiar un costo) para que el grafo se construya de forma distinta.

Este módulo solo conoce la interfaz GrafoBase (ver grafo_base.py), así que
funciona sin cambios sin importar qué representación concreta elija el
equipo.
"""

import config


def costo_horizontal(calle):
    """Costo de una cuadra caminada en sentido oriente-occidente, es decir,
    a lo largo de una calle. Considera las calles con costo especial."""
    return config.CALLES_ESPECIALES.get(calle, config.COSTO_BASE)


def costo_vertical(carrera):
    """Costo de una cuadra caminada en sentido norte-sur, es decir, a lo
    largo de una carrera. Considera las carreras con costo especial."""
    return config.CARRERAS_ESPECIALES.get(carrera, config.COSTO_BASE)


def construir_grafo(grafo):
    """Llena `grafo` (una instancia de una subclase de GrafoBase) con todos
    los vértices y aristas de la cuadrícula definida en config.py, y lo
    retorna para poder encadenar llamadas.

    Cada vértice es la tupla (calle, carrera).
    """
    calles = list(range(config.CALLE_MIN, config.CALLE_MAX + 1))
    carreras = list(range(config.CARRERA_MIN, config.CARRERA_MAX + 1))

    # Vértices: todas las intersecciones calle-carrera de la cuadrícula.
    for calle in calles:
        for carrera in carreras:
            grafo.agregar_vertice((calle, carrera))

    # Aristas horizontales: caminar a lo largo de una calle, entre dos
    # carreras consecutivas.
    for calle in calles:
        for i in range(len(carreras) - 1):
            origen = (calle, carreras[i])
            destino = (calle, carreras[i + 1])
            grafo.agregar_arista(origen, destino, costo_horizontal(calle))

    # Aristas verticales: caminar a lo largo de una carrera, entre dos
    # calles consecutivas.
    for carrera in carreras:
        for i in range(len(calles) - 1):
            origen = (calles[i], carrera)
            destino = (calles[i + 1], carrera)
            grafo.agregar_arista(origen, destino, costo_vertical(carrera))

    return grafo
