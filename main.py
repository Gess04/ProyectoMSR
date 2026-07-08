"""
main.py
========
Punto de entrada del proyecto "Javier y Andreína en Bogotá".

Se ha implementado un menú interactivo que permite modificar la cuadrícula 
(agregar locales o cambiar costos de calles por tráfico/daños) en tiempo
de ejecución, demostrando la flexibilidad de la Lista de Adyacencia.
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

# Se utiliza la Lista de Adyacencia por su eficiencia en memoria y
# facilidad para actualizar pesos en tiempo de ejecución.
from grafo_lista_adyacencia import GrafoListaAdyacencia as RepresentacionGrafo


def mostrar_menu():
    print("\n" + "="*45)
    print(" JAVIER Y ANDREÍNA EN BOGOTÁ - MENÚ ")
    print("="*45)
    print("1. Planificar encuentro (Ej ecutar Algoritmo)")
    print("2. Agregar un nuevo local / punto de encuentro")
    print("3. Modificar el costo de una cuadra (Tráfico/Obstáculo)")
    print("4. Salir")
    return input("Elige una opción: ").strip()


def main():
    # 1. Construimos el grafo base al iniciar el programa
    grafo = construir_grafo(RepresentacionGrafo())

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            # --- OPCIÓN 1: LÓGICA ORIGINAL DE BÚSQUEDA ---
            print("\nEstablecimientos disponibles:")
            for nombre in listar_establecimientos():
                print(f"  - {nombre}")

            destino_texto = input("\n¿A qué establecimiento desean llegar? ").strip()
            destino = buscar_establecimiento(destino_texto)

            if destino is None:
                print("Ese establecimiento no está registrado.")
                continue

            resultado = planificar_encuentro(
                grafo,
                config.DOMICILIOS["javier"],
                config.DOMICILIOS["andreina"],
                destino,
            )

            if resultado is None:
                print("No fue posible encontrar una ruta para ambos hacia ese destino.")
                continue

            print("\n" + "-"*40)
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
                    "rutas no compartan ninguna cuadra dentro del límite de intentos."
                )

        elif opcion == "2":
            # --- OPCIÓN 2: AGREGAR UN LOCAL EN TIEMPO DE EJECUCIÓN ---
            print("\n--- Agregar Nuevo Establecimiento ---")
            nombre = input("Nombre del local (ej. La Defensa): ").strip().lower()
            try:
                calle = int(input("Calle (ej. 52): "))
                carrera = int(input("Carrera (ej. 14): "))
                
                # Validamos que esté dentro de la cuadrícula
                if (config.CALLE_MIN <= calle <= config.CALLE_MAX and 
                    config.CARRERA_MIN <= carrera <= config.CARRERA_MAX):
                    
                    # Al modificar config.ESTABLECIMIENTOS aquí, se queda guardado en memoria 
                    # para el resto de la ejecución y la función buscar_establecimiento() lo encontrará.
                    config.ESTABLECIMIENTOS[nombre] = (calle, carrera)
                    print(f"'{nombre}' agregado exitosamente en la intersección ({calle}, {carrera})!")
                else:
                    print("Error: Las coordenadas están fuera de los límites de la cuadrícula de Bogotá permitida.")
            except ValueError:
                print("Error: Por favor ingresa números enteros válidos para calle y carrera.")

        elif opcion == "3":
            # --- OPCIÓN 3: CAMBIAR COSTO DE UNA CUADRA ---
            print("\n--- Modificar Costo por Tráfico u Obstáculo ---")
            print("Indica la cuadra específica (origen y destino) a modificar:")
            try:
                c1 = int(input("Origen - Calle: "))
                k1 = int(input("Origen - Carrera: "))
                c2 = int(input("Destino - Calle: "))
                k2 = int(input("Destino - Carrera: "))
                nuevo_peso = int(input("Nuevo tiempo a tardar en minutos (ej. 15): "))

                origen = (c1, k1)
                destino = (c2, k2)

                # Validar que los vértices existan en el grafo antes de conectarlos
                if grafo.existe_vertice(origen) and grafo.existe_vertice(destino):
                    # Usamos el mismo método agregar_arista para sobrescribir el peso en memoria.
                    grafo.agregar_arista(origen, destino, nuevo_peso, bidireccional=True)
                    print(f"¡Tráfico actualizado! El nuevo costo entre {origen} y {destino} es de {nuevo_peso} minutos.")
                else:
                    print("Error: Alguna de las intersecciones no existe en el grafo actual.")
            except ValueError:
                print("Error: Por favor ingresa números enteros válidos.")

        elif opcion == "4":
            print("\nSaliendo del planificador... ¡Mucho éxito en la defensa del proyecto!")
            break

        else:
            print("Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    main()