"""Esta clase implementa los métodos necesarios para interactuar con el sistema operativo"""

import os
import json


def importararchivospropiedades():
    rutabase = str(os.path.dirname(os.path.abspath(__file__)))
    if os.name == 'posix':
        rutarelativa = "/propieties/problema.json"
    elif os.name == 'nt':
        rutarelativa = "\propieties\problema.json"
    else:
        raise OSError("No se reconoce este sistema operativo. No se puede importar las configuraciones")
    ruta = rutabase + rutarelativa
    problema = {}
    if os.path.isfile(ruta):
        with open(ruta, 'r') as archivo:
            try:
                problema = json.load(archivo)
            except json.decoder.JSONDecodeError as e:
                raise e
        print(problema)
    else:
        raise FileNotFoundError("No existe el archivo {}".format(str(ruta)))
    return problema
