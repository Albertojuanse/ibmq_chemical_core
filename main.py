"""Ejecución principal"""


def main(mododeejecucion=None):
    """Ejecución principal"""
    if mododeejecucion:
        import ibmq_chemical_core
        ibmq_chemical_core.orquestador.ejecutar()
    elif not mododeejecucion:
        # from ibmq_chemical_web import aplicacion
        # aplicacion.run(port=8080)

        import ibmq_chemical_grafica
        ibmq_chemical_grafica.frontal.main()

        from ibmq_chemical_api import api
        api.run(port=9090)


if __name__ == "__main__":
    main()
