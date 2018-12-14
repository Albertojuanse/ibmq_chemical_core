from flask import Flask

la_api = Flask(__name__)
la_api.config["SECRET_KEY"] = "clave secreta"

from ibmq_chemical_api import api
