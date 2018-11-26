"""Esta clase crea un gestor de las conexiones con las máquinas cuánticas de IBM y los simuladores de Quiskit"""
# Conexiones por arquitectura
import Controlador

# importa módulos
from qiskit import IBMQ, Aer
import time

# Variables globales
__servidoresreales = []
__servidoressimuladores = []

def __cargarcredenciales():
    """Esta función establece conexión con los servidores de IBMQ"""
    cargadas = False
    while not cargadas:
        try:
            IBMQ.load_accounts()
            Controlador.comunicarExito("Se ha establecido conexión con IBMQ")
            cargadas = True
        except:
            Controlador.comunicarExcepcion("Ha fallado la conexión con IBMQ", "Se reintentará en 3 segundos")
            time.sleep(3)

def cargarservidores():
    """Esta función carga los servidores disponibles"""
    Controlador.comunicarexito("Cargando servidores cuánticos disponibles...")
    __cargarcredenciales()

    __servidoresreales = IBMQ.backends()
    __servidoressimuladore = Aer.backends()


def getservidoresreales():
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
