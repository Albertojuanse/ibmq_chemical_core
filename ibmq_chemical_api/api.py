"""Este modulo desarrolla una API del núcleo de la aplicación"""

# Conexiones por arquitectura
import ibmq_chemical_core
import ibmq_chemical_comun

# Dependencias
from ibmq_chemical_api import la_api
from flask import Response, abort, request

import json


# Recursos comunes
@la_api.route("/servidores", methods=["GET"])
def servidores_get():
    """Esta función devuelve los servidores que el usuario puede escoger"""
    servidoresreales, servidoressimuladores, servidor = ibmq_chemical_core.orquestador.obtener_backends()
    servidores = {"servidoresreales": servidoresreales, 
                  "servidoressimuladores": servidoressimuladores, 
                  "servidor actual": servidor
                  }
    respuesta = _crear_json_resultados(servidores)
    return Response(respuesta, status=200, mimetype='application/json', headers={'content-type': 'application/json'})


@la_api.route("/servidores", methods=["POST"])
def servidores_post():
    """Esta función configura en el orquestador un servidor concreto"""
    configuracion = request.get_json()
    resultado = ibmq_chemical_core.orquestador.configurar_backend(configuracion["servidor"])
    if resultado:
        return Response(status=200)
    else:
        abort(422, "Error 422: El nombre de servidor no coincide con ninguno accesible")


# Recursos de cálculos
@la_api.route("/ejecutar_ibmq_vqe", methods=["POST"])
def ejecutar_ibmq_vqe_post():
    """Esta función permite realiza el cálculo del VQE en Qiskit Aqua de IBMQ"""
    configuracion = request.get_json()
    configuracionproblema = configuracion["problema"]
    configuracionmolecula = configuracion["molecula"]
    configuracioncore = {}
    if "core" in configuracion:
        configuracioncore = configuracion["core"]
    if "dibujo" in configuracioncore:
        dibujo = configuracioncore["dibujo"]
    else:
        dibujo = None

    resultados, consola, distancias = ibmq_chemical_core.orquestador.ejecutar_ibmq_vqe(
        configuracionproblema=configuracionproblema,
        configuracionmolecula=configuracionmolecula,
        dibujo=dibujo
    )
    respuesta = _crear_json_resultados(resultados, consola, distancias)
    return Response(respuesta, status=200, mimetype='application/json', headers={'content-type': 'application/json'})


@la_api.route("/ejecutar_numero_aleatorio", methods=["GET"])
def ejecutar_numero_aleatorio_get():
    """Esta función deuelve al usuario un objeto JSON con un número aleatorio de las cifras requeridas"""
    configuracion = request.get_json()
    cifras = configuracion["cifras"]
    if "backend" in configuracion:
        backend = ibmq_chemical_core.orquestador.set_backend(configuracion["backend"])
    else:
        backend = None
    resultado = ibmq_chemical_core.orquestador.ejecutar_numero_aleatorio(cifras, servidor=backend)
    respuesta = _crear_json_resultados(resultado)
    return Response(respuesta, status=200, mimetype='application/json', headers={'content-type': 'application/json'})


# Internas de la API
def _crear_json_servidores(servidores, consola=None):
    """Esta función encapsula en un archivo JSON los listados de servidores"""
    nombre = ibmq_chemical_comun.interfazsistema.generar_nombre()

    archivo = {"nombre": nombre,
               "servidores": servidores,
               "consola": consola
               }
    return json.dumps(archivo)


def _crear_json_resultados(resultado, consola=None, distancia=None):
    """Esta función encapsula en un archivo JSON algún cálculo"""
    nombre = ibmq_chemical_comun.interfazsistema.generar_nombre()

    archivo = {"nombre": nombre,
               "resultado": resultado,
               "consola": consola,
               "distancias": distancia
               }
    return json.dumps(archivo)
