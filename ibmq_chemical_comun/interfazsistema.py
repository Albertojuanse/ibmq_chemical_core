"""Esta clase implementa los métodos necesarios para interactuar con el sistema operativo"""

from dependencies import lectorjson

def importar_propiedades(carpeta, archivo):
    """Esta función importa un JSON"""
    return lectorjson.importar_propiedades(carpeta, archivo)

def exportar_propiedades(carpeta, archivo, propiedades):
    """Esta función exporta un JSON"""
    return lectorjson.exportar_propiedades(carpeta, archivo, propiedades)
