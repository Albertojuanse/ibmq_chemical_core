from flask import Flask

api = Flask('api', __name__)

from ibmq_chemical_api import api
