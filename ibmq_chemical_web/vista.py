"""Este módulo hace de vista de la aplicación web"""

# Conexiones por arquitectura
from ibmq_chemical_web import modelo, controlador
from ibmq_chemical_web import aplicacion

# Dependencias
from flask import render_template, Response, stream_with_context


# http://flask.pocoo.org/docs/1.0/patterns/streaming/
# Definiciones


def stream_template(template_name, **context):
    aplicacion.update_template_context(context)
    t = aplicacion.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


def generate():
    while True:
        yield "Consola"+"<br>"


def index():
    """Esta función devuelve al usuario la página de index"""
    return render_template("index.html", title="IBMQ chemical")


def ejecutado():
    """Esta función indica al usuario que se está ejecutando el algoritmo"""
    lineas = modelo.get_consola()
    print(lineas)
    return render_template("resultados.html", title="IBMQ chemical", ejecutado=True, lineas=lineas)

    #return Response(stream_with_context(mensaje))
    #return Response(stream_template("index.html"), lineas=lineas)
    #return render_template("index.html", lineas=lineas)
    #return Response(render_template("resultados.html", ejecutado=True))
    #return Response(stream_with_context("Ejecutandose"))
