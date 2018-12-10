from dependencies import lectorjson

if __name__ == "__main__":
    mododeejecucion = lectorjson.importar_propiedades("properties", "modo.json")["modo"]

    if mododeejecucion == "linea de comandos":
        import ibmq_chemical_core
        import ibmq_chemical_comun
        ibmq_chemical_core.orquestador.ejecutar(mododeejecucion)

    elif mododeejecucion == "aplicacion web":
        from ibmq_chemical_web import aplicacion

        aplicacion.run()
