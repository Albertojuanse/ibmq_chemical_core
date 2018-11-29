"""Esta clase implementa los métodos necesarios para interactuar con el sistema operativo"""

import os
import json


def __generarruta(carpeta, archivo):
    rutabase = str(os.path.dirname(os.path.abspath(__file__)))
    rutarelativa = os.path.join(carpeta, archivo)
    return rutabase + rutarelativa


def importarpropiedades(carpeta, archivo):
    ruta = __generarruta(carpeta, archivo)
    with open(ruta, "r") as archivo:
        problema = json.load(archivo)
    print(problema)
