"""Esta clase implementa los métodos necesarios para interactuar con el sistema operativo"""

import os
import json
from collections import OrderedDict


def __generarruta(carpeta, archivo):
    rutabase = str(os.path.dirname(os.path.abspath(__file__)))
    rutarelativa = os.path.join(carpeta, archivo)
    return os.path.join(rutabase, rutarelativa)


def importarpropiedades(carpeta, archivo):
    ruta = __generarruta(carpeta, archivo)
    with open(ruta, "r") as archivo:
        propiedades = json.load(archivo)
    return propiedades


def exportarpropiedades(carpeta, archivo, propiedades):
    ruta = __generarruta(carpeta, archivo)
    with open(ruta, "w") as archivo:
        json.dump(propiedades, archivo)
