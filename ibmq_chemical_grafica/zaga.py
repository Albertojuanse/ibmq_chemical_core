"""Este modulo implementa el back-end de la aplicación gráfica"""

# Conexiones por arquitectura
from ibmq_chemical_grafica import frontal

# Dependencias
import json
import requests


def ejecutar_ibmq_vqe(molecula, problema, ventana_frontal):
    """Esta función invoca la ejecución del orquestador con los datos de la aplicacion gráfica a través de la API"""
    peticion = {"molecula": molecula, "problema": problema}
    headers = {'content-type': 'application/json'}
    respuesta_api = requests.post("http://127.0.0.1:9090/ejecutar_ibmq_vqe", headers=headers, data=json.dumps(peticion))
    print("Respuesta en zaga: {}".format(respuesta_api.json()))
    ventana_frontal.mostrar_resultados(respuesta_api.json())
