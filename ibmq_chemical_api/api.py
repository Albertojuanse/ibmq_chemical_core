"""Este modulo desarrolla una API del núcleo de la aplicación"""

# Conexiones por arquitectura
import ibmq_chemical_core

# Dependencias
from ibmq_chemical_api import api
from flask import request, redirect

consola = []
resultados = {"resultados": ""}


@api.route("/", methods=["GET"])
def index():
    """Esta función solicita a la API el calculo"""
    configuracionmolecula = request.get_json()
    ibmq_chemical_core.orquestador.ejecutar(configuracionmolecula)
    consola = get_consola()
    resultados = {"consola": consola}
    return resultados


def mostrar_mensaje_consola(mensaje):
    consola.append(mensaje)


def get_consola():
    return consola


def get_resultados():
    return resultados
