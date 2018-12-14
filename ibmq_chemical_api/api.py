"""Este modulo desarrolla una API del núcleo de la aplicación"""

# Conexiones por arquitectura
import ibmq_chemical_core
import ibmq_chemical_comun

# Dependencias
from ibmq_chemical_api import la_api
from flask import Response, request

import json


@la_api.route("/ejecutar_ibmq_vqe", methods=["POST"])
def ejecutar_ibmq_vqe_post():
    """Esta función permite realiza el cálculo del VQE en Qiskit Aqua de IBMQ"""
    configuracion = request.get_json()
    configuracionproblema = configuracion["problema"]
    configuracionmolecula = configuracion["molecula"]
    resultados, consola = ibmq_chemical_core.orquestador.ejecutar_ibmq_vqe(configuracionproblema, configuracionmolecula)
    respuesta = _crear_json_resultados(resultados, consola)
    print("Respuesta: {}".format(respuesta))
    return Response(respuesta, status=200, mimetype='application/json', headers={'content-type': 'application/json'})


@la_api.route("/servidores", methods=["GET"])
def servidores_get():
    """Esta función devuelve los backend que el usuario puede escoger"""
    servidoresreales, servidoressimuladores = ibmq_chemical_core.orquestador.obtener_backends()
    servidores = {"servidoresreales": servidoresreales, "servidoressimuladores": servidoressimuladores}
    respuesta = _crear_json_resultados(servidores)
    return Response(respuesta, status=200, mimetype='application/json', headers={'content-type': 'application/json'})


@la_api.route("/ejecutar_numero_aleatorio", methods=["GET"])
def ejecutar_numero_aleatorio_get():
    """Esta función deuelve al usuario un objeto JSON con un número aleatorio de las cifras requeridas"""
    cifras = request.form.get("cifras")
    backend = request.form.get("backend")
    resultado = ibmq_chemical_core.orquestador.ejecutar_numero_aleatorio(cifras, backend)
    respuesta = _crear_json_resultados(resultado)
    print("Respuesta: {}".format(respuesta))
    return Response(respuesta, status=200, mimetype='application/json', headers={'content-type': 'application/json'})


def _crear_json_resultados(resultado, consola=None):
    """Esta función encapsula en un archivo JSON algún cálculo"""
    nombre = ibmq_chemical_comun.interfazsistema.generar_nombre()

    archivo = {"nombre": nombre,
               "resultado": resultado,
               "consola": consola
               }
    return json.dumps(archivo)
