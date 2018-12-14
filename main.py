"""Ejecución principal"""

from threading import Thread
from flask import Flask


class ibmq_chemical_api_Hilo(Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        from ibmq_chemical_api import la_api
        la_api.run(port=self.port)


class ibmq_chemical_web_Hilo(Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        from ibmq_chemical_web import aplicacion
        aplicacion.run(port=self.port)


class ibmq_chemical_grafica_Hilo (Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        import ibmq_chemical_grafica
        ibmq_chemical_grafica.frontal.main()


def main(mododeejecucion=None):
    """Ejecución principal"""
    """
    if mododeejecucion:
        import ibmq_chemical_core
        ibmq_chemical_core.orquestador.ejecutar()
    elif not mododeejecucion:
    """


    # Inicializar hilos
    icwH = ibmq_chemical_web_Hilo(8080)
    icgH = ibmq_chemical_grafica_Hilo()
    icaH = ibmq_chemical_api_Hilo(9090)

    # Lanzar hilos
    icgH.start()
    icwH.start()
    icaH.start()


if __name__ == "__main__":
    main()
