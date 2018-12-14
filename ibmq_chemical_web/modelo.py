"""Este módulo hace de modelo y servirá de enlace con el orquestador"""

# Conexiones por arquitectura
import ibmq_chemical_core
from ibmq_chemical_web import controlador, vista

# Dependencias
from flask import redirect
import requests
import json

consola = []
resultados = {"resultados": ""}


def ejecutar_ibmq_vqe(request):
    """Esta función invoca la ejecución del orquestador con los datos de la aplicacion web a través de la API"""
    molecula = {'driver': 'PYSCF',
                             'configuracion': {
                                 'properties': {
                                   'atom': 'Li .0 .0 .0; H .0 .0 1.6',
                                   'unit': 'Angstrom',
                                   'charge': 0,
                                   'spin': 0,
                                   'basis': 'sto3g'}
                                }
                             }
    molecula["configuracion"]["properties"]["atom"] = request.form.get("estructura")
    molecula["configuracion"]["properties"]["unit"] = request.form.get("unidades")
    molecula["configuracion"]["properties"]["charge"] = request.form.get("carga")
    molecula["configuracion"]["properties"]["spin"] = request.form.get("espin")
    molecula["configuracion"]["properties"]["base"] = request.form.get("base")

    problema = {"general": {"tipo_de_mapeo": "parity"},
                "COBYLA": {"max_eval": 200},
                "UCCSD": {"profundidad": 1,
                          "orbitales_activos_ocupados": [0],
                          "orbitales_activos_no_ocupados": [0, 1],
                          "numero_de_slices": 1
                          }
                }

    peticion = {"molecula": molecula, "problema": problema}
    headers = {'content-type': 'application/json'}
    respuesta_api = requests.post("http://127.0.0.1:9090/ejecutar_ibmq_vqe", headers=headers, data=json.dumps(peticion))
    return vista.mostrar_resultados_ibmq_vqe(respuesta_api.json())


def mostrar_mensaje_consola(mensaje):
    consola.append(mensaje)


def get_consola():
    return consola


def get_resultados():
    return resultados
