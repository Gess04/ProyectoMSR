"""
grafo_lista_adyacencia.py
=========================
Implementación definitiva del grafo utilizando una Lista de Adyacencia.

Se optó por utilizar un diccionario de diccionarios de la forma:
{ vertice_origen: { vertice_destino: peso, ... } }

Justificación para la defensa:
1. Eficiencia de memoria: Al ser un grafo de cuadrícula, es un grafo disperso. 
   No gastamos memoria en conexiones inexistentes.
2. Eficiencia de tiempo: Buscar los vecinos de un vértice es O(1), ideal para Dijkstra.
3. Flexibilidad dinámica: Permite agregar nuevos vértices (locales) y actualizar 
   costos en tiempo de ejecución simplemente reasignando valores en el diccionario.
"""

from grafo_base import GrafoBase

class GrafoListaAdyacencia(GrafoBase):
    def __init__(self):
        # El diccionario principal que almacena el grafo
        self._adyacencia = {}

    def agregar_vertice(self, vertice):
        """Agrega un vértice al grafo si todavía no existe."""
        if vertice not in self._adyacencia:
            self._adyacencia[vertice] = {}

    def agregar_arista(self, origen, destino, peso, bidireccional=True):
        """
        Agrega una arista con un peso entre dos vértices.
        
        NOTA: Este mismo método sirve para ACTUALIZAR costos en tiempo 
        de ejecución. Si la arista ya existe, simplemente sobrescribe 
        el peso anterior con el nuevo.
        """
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        
        self._adyacencia[origen][destino] = peso
        
        if bidireccional:
            self._adyacencia[destino][origen] = peso

    def vecinos(self, vertice):
        """Retorna un iterable de tuplas (vecino, peso)"""
        # .items() retorna directamente la tupla (vecino, peso) del diccionario interno
        return self._adyacencia.get(vertice, {}).items()

    def vertices(self):
        """Retorna un iterable con todos los vértices del grafo."""
        return self._adyacencia.keys()

    def existe_vertice(self, vertice):
        """Indica si el vértice ya fue agregado al grafo."""
        return vertice in self._adyacencia

    def peso(self, origen, destino):
        """
        Retorna el peso de la arista origen -> destino, o None si esa
        arista no existe.
        """
        return self._adyacencia.get(origen, {}).get(destino)