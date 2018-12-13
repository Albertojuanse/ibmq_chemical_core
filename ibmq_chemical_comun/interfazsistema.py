"""Esta clase implementa los métodos necesarios para interactuar con el sistema operativo"""

import os
import time
import json


def importar_propiedades(carpeta, archivo):
    """Esta función importa un diccionario de un archivo JSON"""
    ruta = __generar_ruta(carpeta, archivo)
    with open(ruta, "r") as archivo:
        propiedades = json.load(archivo)
    return propiedades


def exportar_propiedades(carpeta, archivo, propiedades):
    """Esta función exporta un diccionario a un archivo JSON"""
    ruta = __generar_ruta(carpeta, archivo)


def guardar_resultados(resultados):
    """Esta función permite guardar en el sistema un archivo json con un resultado"""
    nombrearchivo = generar_nombre() + ".json"
    ruta = __generar_ruta("resultados", nombrearchivo)

    if not os.path.exists(__generar_ruta("resultados")):
        os.mkdir(__generar_ruta("resultados"))
    with open(ruta, "w") as archivo:
        json.dump(resultados, archivo)


def generar_propieties_por_defecto():
    molecula = {"driver": "PYSCF",
                "configuracion":
                    {"properties":
                        {"atom": "Li .0 .0 .0; H .0 .0 1.6",
                         "unit": "Angstrom",
                         "charge": 0,
                         "spin": 0,
                         "basis": "sto3g"}
                     }
                }
    problema = {"general": {"tipo_de_mapeo": "parity"},
                "COBYLA": {"max_eval": 200},
                "UCCSD": {"profundidad": 1,
                          "orbitales_activos_ocupados": [0],
                          "orbitales_activos_no_ocupados": [0, 1],
                          "numero_de_slices": 1
                          }
                }

    resultados = {}

    if not os.path.exists(__generar_ruta("properties")):
        os.mkdir(__generar_ruta("properties"))

    exportar_propiedades("properties", "molecula.json", molecula)
    exportar_propiedades("properties", "problema.json", problema)
    exportar_propiedades("properties", "resultados.json", resultados)


def generar_nombre():
    """Esta función genera nombre para los archivos usando para ello la hora y fecha actual del sistema"""
    nombre = str(time.localtime().tm_year) +\
             str(time.localtime().tm_mon) + \
             str(time.localtime().tm_mday) + \
             str(time.localtime().tm_hour) + \
             str(time.localtime().tm_min) + \
             str(time.localtime().tm_sec)
    return nombre


def __generar_ruta(carpeta, archivo=None):
    """Esta función devuelve la ruta en la cual está el archivo que se desea modificar"""
    rutabasedependencies = str(os.path.dirname(os.path.abspath(__file__)))
    rutabase = os.path.abspath(os.path.join(rutabasedependencies, os.pardir))
    if archivo:
        rutarelativa = os.path.join(carpeta, archivo)
    else:
        rutarelativa = os.path.join(carpeta, "")
    return os.path.join(rutabase, rutarelativa)
