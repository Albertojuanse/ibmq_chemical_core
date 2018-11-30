"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
import interfazdeusuario
import interfazsistema
import interfazdemodulos
import gestortrasero
from gestordetareas import GestorDeTareas

# Dependencias
import time
import json

# ## Ejecución principal ##

# Se cargan las credenciales, se establece la conexión con IBMQ y se cargan los listados de servidores
interfazdeusuario.bienvenida()
credendialescargadas = False
while not credendialescargadas:
    if gestortrasero.cargarservidores():
        credendialesCargadas = True
    else:
        time.sleep(3)
    interfazdeusuario.mostrarcredenciales(credendialescargadas)

# Lectura del los archivos de configuración del problema
configuraciondriver = interfazsistema.importarpropiedades("properties", "molecula.json")
#configuracionaqua = interfazsistema.importarpropiedades("properties", "problema.json")

# Paso 1: cálculo de la molécula
molecula = interfazdemodulos.procesarmolecula(configuraciondriver)
print(molecula)
