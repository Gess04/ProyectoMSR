"""
config.py
===========
Único lugar del proyecto donde viven los DATOS del problema.

Ningún otro módulo contiene calles, carreras, costos ni direcciones
"quemadas" en el código: todos se leen desde aquí. Esto permite, por
ejemplo, agregar un nuevo sitio de encuentro el día de la defensa
simplemente añadiendo una línea a ESTABLECIMIENTOS, sin tocar el resto
del programa.

Convención de vértices
-----------------------
Cada intersección se representa como la tupla (calle, carrera).
Por ejemplo, la Calle 54 con Carrera 14 es el vértice (54, 14).
"""

# ---------------------------------------------------------------------------
# Límites de la cuadrícula donde se ubican los establecimientos
# (Calle 50 al sur, Calle 55 al norte, Carrera 10 al este, Carrera 15 al
# oeste), tal como se describe en el enunciado.
# ---------------------------------------------------------------------------
CALLE_MIN = 50
CALLE_MAX = 55
CARRERA_MIN = 10
CARRERA_MAX = 15

# ---------------------------------------------------------------------------
# Costos de caminata (en minutos) por cuadra.
# ---------------------------------------------------------------------------
# Costo de una cuadra "normal".
COSTO_BASE = 5

# Calles cuyo costo por cuadra es distinto del costo base. Se aplica a las
# cuadras que se caminan A LO LARGO de esa calle (sentido oriente-occidente).
# La Calle 51 tiene mucha actividad comercial: 10 minutos por cuadra.
CALLES_ESPECIALES = {
    51: 10,
}

# Carreras cuyo costo por cuadra es distinto del costo base. Se aplica a las
# cuadras que se caminan A LO LARGO de esa carrera (sentido norte-sur).
# Las carreras 11, 12 y 13 tienen aceras en mal estado: 7 minutos por cuadra.
CARRERAS_ESPECIALES = {
    11: 7,
    12: 7,
    13: 7,
}

# ---------------------------------------------------------------------------
# Domicilios de la pareja.
# ---------------------------------------------------------------------------
DOMICILIOS = {
    "javier": (54, 14),     # Calle 54 con Carrera 14
    "andreina": (52, 13),   # Calle 52 con Carrera 13
}

# ---------------------------------------------------------------------------
# Establecimientos donde se pueden encontrar. Se puede agregar uno nuevo
# (por ejemplo, el día de la defensa) simplemente añadiendo una entrada
# aquí, siempre y cuando su intersección quede dentro de la cuadrícula
# definida por CALLE_MIN/CALLE_MAX/CARRERA_MIN/CARRERA_MAX.
# ---------------------------------------------------------------------------
ESTABLECIMIENTOS = {
    "the darkness": (50, 14), 
    "la pasion": (54, 11),  
    "mi rolita": (50, 12),
    "UNIMET":(52, 13)      
}
