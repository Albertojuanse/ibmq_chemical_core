from flask import Flask

aplicacion = Flask(__name__)
aplicacion.config["SECRET_KEY"] = "clave secreta"

from ibmq_chemical_web import controlador
