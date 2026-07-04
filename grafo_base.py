"""
Define la interfaz (contrato) que debe cumplir cualquier representación de
grafo utilizada en el proyecto.

El equipo todavía no ha decidido cuál de las representaciones vistas en
clase va a usar (matriz de adyacencia, lista de adyacencia, lista de
aristas, matriz de incidencia o lista de incidencia). Por esa razón, el
resto del programa —constructor_grafo.py, dijkstra.py y planificador.py—
NUNCA accede directamente a una estructura de datos concreta: solo conoce
esta interfaz (esto es polimorfismo: programar contra una abstracción,
no contra una implementación).

Cuando decidan la representación definitiva, basta con crear una clase que
herede de GrafoBase e implemente estos métodos. Ningún otro archivo del
proyecto deberá modificarse; solo hay que cambiar una línea en main.py que
indica qué clase concreta se está usando.
"""

from abc import ABC, abstractmethod


class GrafoBase(ABC):

    @abstractmethod
    def agregar_vertice(self, vertice):
        """Agrega un vértice al grafo si todavía no existe."""
        raise NotImplementedError

    @abstractmethod
    def agregar_arista(self, origen, destino, peso, bidireccional=True):
        """Agrega una arista con un peso (costo en minutos) entre dos
        vértices. Si bidireccional es True, también agrega la arista en
        sentido contrario (destino -> origen) con el mismo peso, ya que en
        este problema las calles se pueden caminar en ambos sentidos."""
        raise NotImplementedError

    @abstractmethod
    def vecinos(self, vertice):
        """Retorna un iterable de tuplas (vecino, peso) """
        raise NotImplementedError

    @abstractmethod
    def vertices(self):
        """Retorna un iterable con todos los vértices del grafo."""
        raise NotImplementedError

    @abstractmethod
    def existe_vertice(self, vertice):
        """Indica si el vértice ya fue agregado al grafo."""
        raise NotImplementedError

    @abstractmethod
    def peso(self, origen, destino):
        """Retorna el peso de la arista origen -> destino, o None si esa
        arista no existe."""
        raise NotImplementedError
