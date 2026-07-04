"""

Implementación propia del algoritmo de Dijkstra (no se usa ninguna librería
de terceros de grafos/algoritmos), adaptada para poder excluir un conjunto
de aristas "prohibidas" durante la búsqueda.

Esa adaptación es la que permite, en planificador.py, recalcular la ruta de
una persona evitando las cuadras que ya está usando la otra, para que
Javier y Andreína nunca caminen juntos.

Se usa `heapq` como cola de prioridad. `heapq` forma parte de la librería
estándar de Python (no es software de terceros); Dijkstra en sí se
implementa manualmente a continuación.
"""

import heapq


def _arista_prohibida(u, v, prohibidas):
    if not prohibidas:
        return False
    return frozenset((u, v)) in prohibidas


def dijkstra(grafo, origen, destino, prohibidas=None):
    """Calcula el camino de costo (tiempo) mínimo entre `origen` y
    `destino` dentro de `grafo`.

    Parámetros
    ----------
    grafo : GrafoBase
        Grafo sobre el cual se calcula el camino.
    origen, destino : vértices del grafo, con la forma (calle, carrera).
    prohibidas : set opcional de frozenset({u, v}) que representan
        cuadras que NO se pueden usar. Se emplea para obligar a que dos
        caminos no compartan ninguna cuadra.

    Retorna
    -------
    (costo_total, camino) donde `camino` es la lista de vértices desde
    `origen` hasta `destino`, en orden. Si no existe un camino posible
    (por ejemplo, porque las aristas prohibidas lo bloquean por completo),
    retorna (None, None).
    """
    if not grafo.existe_vertice(origen) or not grafo.existe_vertice(destino):
        return None, None

    distancias = {origen: 0}
    previos = {}
    visitados = set()
    cola = [(0, origen)]

    while cola:
        dist_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue
        visitados.add(actual)

        if actual == destino:
            break

        for vecino, peso in grafo.vecinos(actual):
            if _arista_prohibida(actual, vecino, prohibidas):
                continue
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva_dist
                previos[vecino] = actual
                heapq.heappush(cola, (nueva_dist, vecino))

    if destino not in distancias:
        return None, None

    # Reconstrucción del camino recorriendo los predecesores hacia atrás.
    camino = [destino]
    while camino[-1] != origen:
        camino.append(previos[camino[-1]])
    camino.reverse()

    return distancias[destino], camino
