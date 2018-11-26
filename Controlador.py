"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
import InterfazDeUsuario
import InterfazDeModulos
import GestorTrasero
from GestorDeTareas import GestorDeTareas

# Funciones estáticas de supervisión
def comunicarexcepcion(aviso, consecuencia):
    """Esta función se invoca para comunicar una excepción a la interfaz de usuario"""
    InterfazDeUsuario.mostrarmensajeconsola(aviso)
    InterfazDeUsuario.mostrarmensajeconsola(consecuencia)

def comunicarexito(mensaje):
    """Esta función se invoca para comunicar un éxito a la interfaz de usuario"""
    InterfazDeUsuario.mostrarmensajeconsola(mensaje)

# Ejecución principal
InterfazDeUsuario.mostrarmensajeconsola("Bienvenido a ibmq_chemical_core")
GestorTrasero.cargarservidores()
