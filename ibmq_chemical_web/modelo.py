"""Este módulo hace de modelo y servirá de enlace con el orquestador"""

# Conexiones por arquitectura
import ibmq_chemical_core
from ibmq_chemical_web import controlador, vista

# Dependencias
from flask import redirect

consola = []
resultados = {"resultados": ""}


def ejecutar(request):
    """Esta función invoca la ejecución del orquestador con los datos de la aplicacion web"""

    configuracionmolecula = {'driver': 'PYSCF',
                             'configuracion': {
                                 'properties': {
                                   'atom': 'Li .0 .0 .0; H .0 .0 1.6',
                                   'unit': 'Angstrom',
                                   'charge': 0,
                                   'spin': 0,
                                   'basis': 'sto3g'}
                                }
                             }
    configuracionmolecula["configuracion"]["properties"]["atom"] = request.form.get("estructura")
    configuracionmolecula["configuracion"]["properties"]["unit"] = request.form.get("unidades")
    configuracionmolecula["configuracion"]["properties"]["charge"] = request.form.get("carga")
    configuracionmolecula["configuracion"]["properties"]["spin"] = request.form.get("espin")
    configuracionmolecula["configuracion"]["properties"]["base"] = request.form.get("base")
    ibmq_chemical_core.orquestador.ejecutar(configuracionmolecula)
    return redirect("/resultados")


def mostrar_mensaje_consola(mensaje):
    consola.append(mensaje)


def get_consola():
    return consola


def get_resultados():
    return resultados
