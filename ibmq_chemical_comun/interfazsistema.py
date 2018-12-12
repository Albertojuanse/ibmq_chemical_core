"""Esta clase implementa los métodos necesarios para interactuar con el sistema operativo"""

import os
import json


def __generar_ruta(carpeta, archivo):
    """Esta función devuelve la ruta en la cual está el archivo que se desea modificar"""
    rutabasedependencies = str(os.path.dirname(os.path.abspath(__file__)))
    rutabase = os.path.abspath(os.path.join(rutabasedependencies, os.pardir))
    rutarelativa = os.path.join(carpeta, archivo)
    return os.path.join(rutabase, rutarelativa)


def importar_propiedades(carpeta, archivo):
    """Esta función importa un diccionario de un archivo JSON"""
    ruta = __generar_ruta(carpeta, archivo)
    with open(ruta, "r") as archivo:
        propiedades = json.load(archivo)
    return propiedades


def exportar_propiedades(carpeta, archivo, propiedades):
    """Esta función exporta un diccionario a un archivo JSON"""
    ruta = __generar_ruta(carpeta, archivo)
    with open(ruta, "w") as archivo:
        json.dump(propiedades, archivo)
