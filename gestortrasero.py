"""Esta clase crea un gestor de las conexiones con las máquinas cuánticas de IBM y los simuladores de Quiskit"""

# importa módulos
import qiskit

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
        if not servidor.configuration()["simulator"]:
            servidoresreales.append(servidor)
    return servidoresreales


def get_servidores_simuladores():
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
    return __servidoressimuladores


def enviar_circuito():
    pass


def enviar_tarea():
    pass


def recibir_circuito():
    pass


def recibir_tarea():
    pass
