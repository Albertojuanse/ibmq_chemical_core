"""Esta clase crea un gestor de las conexiones con las máquinas cuánticas de IBM y los simuladores de Quiskit"""

# importa módulos
import qiskit
import time

# Variables globales
__servidoresreales = []
__servidoressimuladores = []


def cargar_servidores():
    """Esta función establece conexión con los servidores de IBMQ y los servidores disponibles"""
    try:
        qiskit.IBMQ.load_accounts()
        __servidoresreales = qiskit.IBMQ.backends()
        __servidoressimuladores = qiskit.Aer.backends()
        return True
    except:
        return False


def get_servidores_reales():
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
    # Se precisa eliminar los simuladores de esta lista
    servidoresreales = []
    for servidor in __servidoresreales:
        if not servidor.configuration()["simulator"] and servidor.status()['operational']:
            servidoresreales.append(servidor)
    return servidoresreales


def get_servidores_simuladores():
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
    return __servidoressimuladores


def procesar_circuito(circuito, backend, qubitsminimo=None):
    """Esta función recibe un circuito cuántico, lo trata, y devuelve los resultados"""
    if not backend.status()['operational']:
        raise Exception("La maquina seleccionada para la ejecución está en mantenimiento; repita y escoja otra")

    if qubitsminimo:
        if int(backend.configuration()['n_qubits']) >= qubitsminimo:
            raise Exception("La máquina elegida tiene menos cubits de los necesarios para desplegar el circuito")

    tarea = _enviar_circuito(circuito, backend)
    resultados = _recibir_circuito(tarea, circuito)
    return resultados


def _enviar_circuito(circuito, backend):
    """Esta función envía un circuito al backend deseado"""
    return qiskit.execute(circuito, backend=backend, shots=1000)


def _recibir_circuito(tarea, circuito):
    """Esta función insiste en recolectar los resultados hasta que lo consigue"""
    while True:
        try:
            resultadocompleto = tarea.result(timeout=10)
            if ('status' not in resultadocompleto.keys()):
                resultado = resultadocompleto.get_counts(circuito)
                return resultado
        except:
            time.sleep(5)
