"""

Resuelve el problema central del proyecto: encontrar, para Javier y para
Andreína, dos caminos hacia el mismo establecimiento que:

  1. Minimicen (cada uno por su lado) el tiempo de caminata.
  2. No compartan ninguna cuadra, ya que los dos deben llegar juntos a la
     puerta pero no pueden ser vistos caminando juntos por la calle.
  3. Permitan calcular cuánto tiempo antes debe salir de su casa quien
     tenga el camino más corto, para que ambos lleguen a la puerta del
     establecimiento en el mismo instante.

Se calcula el camino más corto de cada uno por separado y, si comparten alguna cuadra, esa(s)
cuadra(s) se agregan a un conjunto de aristas prohibidas y se vuelve a
correr Dijkstra para ambos. Esto se repite hasta que los caminos dejen de
cruzarse o hasta agotar un número razonable de intentos.
"""

from dijkstra import dijkstra

LIMITE_INTENTOS = 50


def _aristas_del_camino(camino):
    """Convierte un camino (lista de vértices) en el conjunto de cuadras
    (aristas) que utiliza, representadas como frozenset({u, v}) para que no
    importe el sentido en que se camine."""
    return {frozenset((camino[i], camino[i + 1])) for i in range(len(camino) - 1)}


def _hay_conflicto(camino1, camino2):
    """Indica si dos caminos comparten al menos una cuadra."""
    return len(_aristas_del_camino(camino1) & _aristas_del_camino(camino2)) > 0


def planificar_encuentro(grafo, casa_javier, casa_andreina, destino):
    """Calcula las trayectorias sincronizadas y sin cruces de Javier y
    Andreína hacia `destino`.
    """
    prohibidas = set()

    costo_j, camino_j = dijkstra(grafo, casa_javier, destino, prohibidas)
    costo_a, camino_a = dijkstra(grafo, casa_andreina, destino, prohibidas)

    if costo_j is None or costo_a is None:
        return None

    intentos = 0
    while _hay_conflicto(camino_j, camino_a) and intentos < LIMITE_INTENTOS:
        # Solo se prohíben las cuadras que realmente causan el cruce en
        # esta iteración, no todas las cuadras usadas por ambos caminos.
        conflictivas = _aristas_del_camino(camino_j) & _aristas_del_camino(camino_a)
        prohibidas |= conflictivas

        nuevo_costo_j, nuevo_camino_j = dijkstra(grafo, casa_javier, destino, prohibidas)
        nuevo_costo_a, nuevo_camino_a = dijkstra(grafo, casa_andreina, destino, prohibidas)

        if nuevo_costo_j is None or nuevo_costo_a is None:
            # Ya no es posible evitar el cruce sin dejar a alguien sin
            # camino disponible; se conserva el último resultado válido.
            break

        costo_j, camino_j = nuevo_costo_j, nuevo_camino_j
        costo_a, camino_a = nuevo_costo_a, nuevo_camino_a
        intentos += 1

    conflicto_resuelto = not _hay_conflicto(camino_j, camino_a)

    diferencia = abs(costo_j - costo_a)
    if costo_j < costo_a:
        quien_sale_despues = "javier"
    elif costo_a < costo_j:
        quien_sale_despues = "andreina"
    else:
        quien_sale_despues = None

    return {
        "javier": {"camino": camino_j, "costo": costo_j},
        "andreina": {"camino": camino_a, "costo": costo_a},
        "diferencia_salida": diferencia,
        "quien_sale_despues": quien_sale_despues,
        "conflicto_resuelto": conflicto_resuelto,
        "tiempo_total": max(costo_j, costo_a),
    }
