"""Este módulo hace de controlador de la aplicación web"""

# Conexiones por arquitectura
from ibmq_chemical_web import modelo, vista

# Dependencias
from ibmq_chemical_web import aplicacion
from flask import request


@aplicacion.route("/", methods=["GET"])
def index():
    """Esta función solicita a la vista el index"""
    return vista.index()


@aplicacion.route("/", methods=["POST"])
def ejecutar():
    """Esta función recibe los datos del usuario y se los pasa al controlador"""
    return modelo.ejecutar(request)
