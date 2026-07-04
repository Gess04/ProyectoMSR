"""
Punto de entrada del proyecto "Javier y Andreína en Bogotá".

Antes de la entrega final, reemplacen la representación de grafo que se
usa más abajo (sección "REPRESENTACIÓN DEL GRAFO") por la que elija el
equipo. Mientras tanto, se usa grafo_prueba.GrafoPrueba, una implementación
temporal incluida solo para poder probar el resto del proyecto.
"""

import config
from constructor_grafo import construir_grafo
from planificador import planificar_encuentro
from utils import (
    nombre_vertice,
    buscar_establecimiento,
    listar_establecimientos,
    imprimir_camino,
)

# ---------------------------------------------------------------------------
# REPRESENTACIÓN DEL GRAFO
# ---------------------------------------------------------------------------
# Reemplacen la siguiente línea por la representación final que elija el
# equipo (matriz de adyacencia, lista de adyacencia, lista de aristas,
# matriz de incidencia o lista de incidencia). La clase elegida debe
# heredar de GrafoBase (ver grafo_base.py); el resto del proyecto no
# requiere ningún otro cambio.
from grafo_prueba import GrafoPrueba as RepresentacionGrafo


def main():
    grafo = construir_grafo(RepresentacionGrafo())

    print("Establecimientos disponibles:")
    for nombre in listar_establecimientos():
        print(f"  - {nombre}")

    destino_texto = input("\n¿A qué establecimiento desean llegar? ").strip()
    destino = buscar_establecimiento(destino_texto)

    if destino is None:
        print("Ese establecimiento no está registrado en config.py")
        return

    resultado = planificar_encuentro(
        grafo,
        config.DOMICILIOS["javier"],
        config.DOMICILIOS["andreina"],
        destino,
    )

    if resultado is None:
        print("No fue posible encontrar una ruta para ambos hacia ese destino.")
        return

    imprimir_camino("Javier", resultado["javier"]["camino"], resultado["javier"]["costo"])
    imprimir_camino("Andreína", resultado["andreina"]["camino"], resultado["andreina"]["costo"])

    print(f"\nDestino: {nombre_vertice(destino)}")
    print(f"Tiempo total del plan: {resultado['tiempo_total']} minutos")

    if resultado["quien_sale_despues"] is None:
        print("Ambos deben salir de sus casas al mismo tiempo.")
    else:
        persona = "Javier" if resultado["quien_sale_despues"] == "javier" else "Andreína"
        print(
            f"{persona} debe salir {resultado['diferencia_salida']} minutos "
            "más tarde que su pareja, para llegar exactamente al mismo tiempo."
        )

    if not resultado["conflicto_resuelto"]:
        print(
            "\nAdvertencia: no fue posible garantizar por completo que las "
            "rutas no compartan ninguna cuadra dentro del límite de intentos "
            "configurado en planificador.py."
        )


if __name__ == "__main__":
    main()
