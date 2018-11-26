"""Esta clase crea un gestor de las conexiones con las máquinas cuánticas de IBM y los simuladores de Quiskit"""

# importa módulos
from qiskit import IBMQ, Aer

# Variables globales
__servidoresreales = []
__servidoressimuladores = []

def __cargarcredenciales():
    """Esta función establece conexión con los servidores de IBMQ"""
    try:
        IBMQ.load_accounts()
        return True
    except:
        return False

def cargarservidores():
    """Esta función carga los servidores disponibles"""
    __cargarcredenciales()

    __servidoresreales = IBMQ.backends()
    __servidoressimuladores = Aer.backends()


def getservidoresreales():
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
