# Javier y Andreína en Bogotá

Proyecto en Python que resuelve el problema de encuentro de Javier y
Andreína: encontrar la ruta de caminata que debe seguir cada uno desde su
casa hasta un establecimiento nocturno, de forma que:

1. Cada ruta sea la de menor tiempo posible.
2. Los dos caminos **no compartan ninguna cuadra** (no pueden ser vistos
   caminando juntos).
3. Ambos lleguen a la puerta del establecimiento **exactamente al mismo
   tiempo**, indicando quién debe salir antes de su casa y cuántos minutos
   antes.

Todo el proyecto está escrito en Python puro. La única "librería" usada es
`heapq` (cola de prioridad de la librería estándar de Python), necesaria
para que Dijkstra sea eficiente; el algoritmo de Dijkstra en sí está
implementado a mano en `dijkstra.py`.

## Estructura del proyecto

Se usa una sola carpeta, sin subcarpetas, con un archivo por
responsabilidad:

| Archivo                | Responsabilidad                                                                 |
|-------------------------|----------------------------------------------------------------------------------|
| `config.py`             | **Únicos datos del problema**: límites de la cuadrícula, costos especiales, domicilios y establecimientos. Nada más en el proyecto tiene números o direcciones "quemados". |
| `grafo_base.py`         | Interfaz abstracta (`GrafoBase`) que define qué debe saber hacer cualquier representación de grafo. |
| `grafo_lista_adyacencia.py`       | Implementación de `GrafoBase` (lista de adyacencia con diccionarios). |
| `constructor_grafo.py`  | Construye el grafo de la cuadrícula (vértices y aristas con sus costos) a partir de `config.py`, usando únicamente la interfaz `GrafoBase`. |
| `dijkstra.py`           | Algoritmo de Dijkstra implementado desde cero, con soporte para excluir un conjunto de aristas "prohibidas". |
| `planificador.py`       | Lógica de sincronización: calcula las dos rutas, detecta si comparten alguna cuadra, recalcula evitando el cruce, y calcula la diferencia de horario de salida. |
| `utils.py`              | Funciones de formato/presentación (nombres de vértices, búsqueda de establecimientos por nombre). |
| `main.py`               | Punto de entrada: arma el grafo, pide el destino y muestra el resultado. |

## Cómo ejecutar

```bash
python3 main.py
```

El programa mostrará la lista de establecimientos disponibles (tomada de
`config.py`) y pedirá el nombre de uno de ellos. Luego imprime la ruta
completa de Javier, la de Andreína, y quién debe salir antes y por cuántos
minutos.

## ⚠️ Pendiente antes de la entrega: elegir la representación del grafo

El proyecto pide representar el grafo con una de las 5 representaciones
vistas en clase (matriz de adyacencia, lista de adyacencia, lista de
aristas, matriz de incidencia o lista de incidencia). Como el equipo aún no
decide cuál usar, el resto del código (`constructor_grafo.py`,
`dijkstra.py`, `planificador.py`) se programó **contra la interfaz
`GrafoBase`**, sin depender de ninguna estructura de datos concreta.

Mientras tanto, `grafo_prueba.py` provee una implementación de lista de
adyacencia muy simple (un diccionario de diccionarios) solo para que el
programa corra y se pueda probar el resto de la lógica.

### Para agregar la representación definitiva

1. Creen un archivo nuevo, por ejemplo `grafo_matriz_adyacencia.py`.
2. Dentro, definan una clase que herede de `GrafoBase` (importándola desde
   `grafo_base.py`) e implemente sus 6 métodos:
   `agregar_vertice`, `agregar_arista`, `vecinos`, `vertices`,
   `existe_vertice` y `peso`.
3. En `main.py`, cambien la línea:

   ```python
   from grafo_prueba import GrafoPrueba as RepresentacionGrafo
   ```

   por:

   ```python
   from grafo_matriz_adyacencia import GrafoMatrizAdyacencia as RepresentacionGrafo
   ```

4. Listo. Ningún otro archivo necesita cambios: `constructor_grafo.py`,
   `dijkstra.py` y `planificador.py` solo usan los métodos de `GrafoBase`,
   así que funcionan igual sin importar la representación interna. Si lo
   desean, pueden borrar `grafo_prueba.py`.

Si en la defensa quieren comparar dos representaciones (por ejemplo, para
justificar cuál es más eficiente en este caso), pueden crear varias clases
que implementen `GrafoBase` y alternar cuál se importa en `main.py` sin
tocar el resto del proyecto.

## Cómo se modela el problema como grafo

- **Vértices**: cada intersección calle-carrera dentro de la cuadrícula
  (Calle 50 a 55, Carrera 10 a 15), representada como la tupla
  `(calle, carrera)`.
- **Aristas**: cada cuadra que conecta dos intersecciones consecutivas.
  Todas las aristas son bidireccionales (una calle se puede caminar en
  ambos sentidos).
- **Costos** (ver `config.py`):
  - Una cuadra "normal" cuesta 5 minutos.
  - Una cuadra caminada **a lo largo de** la Carrera 11, 12 o 13 cuesta 7
    minutos (aceras en mal estado).
  - Una cuadra caminada **a lo largo de** la Calle 51 cuesta 10 minutos
    (alta actividad comercial).

  Es importante notar que el costo depende de la calle o carrera **por la
  que se camina**, no de la calle/carrera que se cruza. Por eso
  `constructor_grafo.py` distingue entre aristas horizontales (a lo largo
  de una calle) y verticales (a lo largo de una carrera) al asignar el
  costo.

- **Nada hard-coded**: los límites de la cuadrícula, los costos especiales,
  los domicilios y los establecimientos viven todos en `config.py`. El
  constructor del grafo simplemente recorre esos rangos con dos ciclos
  `for`; si alguien cambia los límites de la cuadrícula o agrega una calle
  especial en `config.py`, el grafo se construye automáticamente distinto,
  sin tocar `constructor_grafo.py`.

## Cómo se resuelve la restricción de "no caminar juntos"

`planificador.py` implementa la adaptación de Dijkstra pedida en el
enunciado:

1. Calcula con Dijkstra la ruta más corta de Javier y la de Andreína, cada
   una por separado, hacia el mismo destino.
2. Si las dos rutas comparten alguna cuadra (arista), esas cuadras se
   agregan a un conjunto de "aristas prohibidas" y se vuelve a correr
   Dijkstra para ambos, esta vez evitando esas cuadras.
3. Este proceso se repite (hasta un límite de intentos) mientras sigan
   compartiendo alguna cuadra, agregando en cada vuelta solo las cuadras
   que realmente están en conflicto en ese momento.
4. Una vez que las rutas no comparten ninguna cuadra, se compara el tiempo
   de cada una: quien tenga el camino más corto debe salir de su casa
   **más tarde**, exactamente por la diferencia de tiempo entre ambas
   rutas, para que los dos lleguen a la puerta del establecimiento al
   mismo tiempo.

### Limitación conocida (para mencionar en la defensa)

La solución garantiza que las dos rutas no **comparten ninguna cuadra**.
No modela explícitamente el caso, más difícil, en que dos rutas usan
cuadras distintas pero se cruzan por el mismo vértice en el mismo instante
(por ejemplo, cuando ambos caminos pasan por la misma esquina en momentos
distintos de su recorrido, pero coinciden en el tiempo debido al ajuste de
salida). Dado que el enunciado dice explícitamente que no pueden ser
"vistos caminando juntos" (es decir, recorriendo la misma cuadra al mismo
tiempo), y no prohíbe coincidir brevemente en una esquina, se consideró que
esta modelación es la interpretación razonable del problema. Si el
profesor pide manejar también ese caso, se puede extender
`planificador.py` agregando una verificación temporal por vértice.

## Cómo agregar un nuevo sitio de encuentro (para el día de la defensa)

Basta con agregar una línea en `config.py`, dentro de `ESTABLECIMIENTOS`,
con el nombre del lugar y su intersección como tupla `(calle, carrera)`,
siempre que esa intersección esté dentro de los límites de la cuadrícula
(`CALLE_MIN`/`CALLE_MAX`/`CARRERA_MIN`/`CARRERA_MAX`). No se necesita tocar
ningún otro archivo.

## Posibles extensiones

El enunciado permite usar una librería externa solo para **dibujar** el
grafo (no para representarlo ni para calcular caminos). Si se desea agregar
esa visualización más adelante, se recomienda crear un archivo aparte
(por ejemplo `visualizador.py`) que reciba el grafo ya construido y una
lista de rutas a resaltar, sin modificar `dijkstra.py` ni
`planificador.py`.
