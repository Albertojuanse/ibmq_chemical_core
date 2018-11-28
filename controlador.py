"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
import interfazdeusuario
import interfazdemodulos
import gestortrasero
from gestordetareas import GestorDeTareas

# Dependencias
import time

# ## Ejecución principal ##

# Se cargan las credenciales, se establece la conexión con IBMQ y se cargan los listados de servidores
interfazdeusuario.mostrarmensajeconsola("Bienvenido a ibmq_chemical_core")
interfazdeusuario.mostrarmensajeconsola("Cargando servidores cuánticos disponibles...")

credendialesCargadas = False
while not credendialesCargadas:
    if gestortrasero.cargarservidores():
        interfazdeusuario.mostrarmensajeconsola("Se ha establecido conexión con IBMQ")
    else:
        interfazdeusuario.mostrarmensajeconsola("Ha fallado la conexión con IBMQ\nSe reintentará en 3 segundos")
        time.sleep(3)
