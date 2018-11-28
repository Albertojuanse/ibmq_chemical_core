"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
import interfazdeusuario
import interfazsistema
import interfazdemodulos
import gestortrasero
from gestordetareas import GestorDeTareas

# Dependencias
import time

# ## Ejecución principal ##

# Se cargan las credenciales, se establece la conexión con IBMQ y se cargan los listados de servidores
interfazdeusuario.bienvenida()
credendialescargadas = False
while not credendialesCargadas:
    if gestortrasero.cargarservidores():
        credendialesCargadas = True
    else:
        time.sleep(3)
    interfazdeusuario.mostrarcredenciales(credendialescargadas)

# Lectura del los archivos de configuración del problema

