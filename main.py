import ibmq_chemical_core
import ibmq_chemical_comun
from dependencies import lectorjson

if __name__ == "__main__":
    mododeejecucion = lectorjson.importar_propiedades("properties", "modo.json")["modo"]
    ibmq_chemical_core.controlador.ejecutar(mododeejecucion)
