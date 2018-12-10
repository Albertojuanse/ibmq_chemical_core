"""Este módulo hace de vista de la aplicación web"""

#Conexiones por arquitectura
from ibmq_chemical_web import modelo, controlador

# Dependencias
from flask import render_template


def index():
    """Esta función devuelve al usuario la página de index"""
    return render_template("index.html", name="Alberto")
