"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
import InterfazDeUsuario
import InterfazDeModulos
import GestorTrasero
from GestorDeTareas import GestorDeTareas

# Dependencias
import time

# ## Ejecución principal ##

# Se cargan las credenciales, se establece la conexión con IBMQ y se cargan los listados de servidores
InterfazDeUsuario.mostrarmensajeconsola("Bienvenido a ibmq_chemical_core")
InterfazDeUsuario.mostrarmensajeconsola("Cargando servidores cuánticos disponibles...")

credendialesCargadas = False
while not credendialesCargadas:
    if GestorTrasero.cargarservidores():
        InterfazDeUsuario.mostrarmensajeconsola("Se ha establecido conexión con IBMQ")
    else:
        InterfazDeUsuario.mostrarmensajeconsola("Ha fallado la conexión con IBMQ\nSe reintentará en 3 segundos")
        time.sleep(3)
