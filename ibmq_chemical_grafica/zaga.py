"""Este modulo implementa el back-end de la aplicación gráfica"""

# Dependencias
import json
from flask import request


def ejecutar_vqe(molecula, problema):
    r = request.post("/ejecutar_ibmq_vqe")
    return r
