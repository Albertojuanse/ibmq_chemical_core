from dependencies import lectorjson

# Variables globales de la ejecucion
import config

if __name__ == "__main__":
    mododeejecucion = lectorjson.importar_propiedades("properties", "modo.json")["modo"]
    config.mododeejecucion = mododeejecucion

    if mododeejecucion == "linea de comandos":
        import ibmq_chemical_core
        import ibmq_chemical_comun
        ibmq_chemical_core.orquestador.ejecutar()

    elif mododeejecucion == "aplicacion web":
        from ibmq_chemical_web import aplicacion

        aplicacion.run(port=8080)

    elif mododeejecucion == "api":
        from ibmq_chemical_api import api
