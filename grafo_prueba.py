"""
grafo_prueba.py
=================
IMPORTANTE: esta es una implementación TEMPORAL / DE PRUEBA de GrafoBase.

Se incluye únicamente para poder ejecutar y probar el resto del proyecto
(constructor_grafo.py, dijkstra.py, planificador.py) mientras el equipo
decide cuál de las 5 representaciones vistas en clase va a usar en la
entrega final. Internamente usa una lista de adyacencia basada en un
diccionario, que es la forma más directa de implementar la interfaz.

Cuando decidan la representación definitiva:
  1. Creen un nuevo archivo (por ejemplo grafo_matriz_adyacencia.py) con una
     clase que herede de GrafoBase e implemente sus métodos.
  2. En main.py, cambien la línea
         from grafo_prueba import GrafoPrueba as RepresentacionGrafo
     por
         from <su_nuevo_archivo> import <SuClase> as RepresentacionGrafo
  3. Ningún otro archivo del proyecto necesita modificarse.
  4. Si ya no la necesitan, pueden borrar este archivo.
"""

from grafo_base import GrafoBase


class GrafoPrueba(GrafoBase):
    def __init__(self):
        self._adyacencia = {}

    def agregar_vertice(self, vertice):
        if vertice not in self._adyacencia:
            self._adyacencia[vertice] = {}

    def agregar_arista(self, origen, destino, peso, bidireccional=True):
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self._adyacencia[origen][destino] = peso
        if bidireccional:
            self._adyacencia[destino][origen] = peso

    def vecinos(self, vertice):
        return self._adyacencia.get(vertice, {}).items()

    def vertices(self):
        return self._adyacencia.keys()

    def existe_vertice(self, vertice):
        return vertice in self._adyacencia

    def peso(self, origen, destino):
        return self._adyacencia.get(origen, {}).get(destino)
