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
        credendialescargadas = True
    else:
        time.sleep(3)
    interfazdeusuario.mostrarcredenciales(credendialescargadas)

# Lectura del los archivos de configuración del problema
configuraciondriver = interfazsistema.importarpropiedades("properties", "molecula.json")
configuracionaqua = interfazsistema.importarpropiedades("properties", "problema.json")

# Paso 1: cálculo de la molécula
molecula = interfazdemodulos.procesarmolecula(configuraciondriver)

# Paso 2: preparar el hamiltoniano
propiedadesmolecula = interfazdemodulos.leerpropiedadesmolecula(molecula)
operadores = interfazdemodulos.obteneroperadoreshamiltonianos(propiedadesmolecula, configuracionaqua)
interfazdemodulos.calcularenergiaclasico(propiedadesmolecula, operadores["operadorqubit"], operadores["energy_shift"])

# Paso 3: Configurar problema y cargar de Aqua los algoritmos
cobyla = interfazdemodulos.configurarCOBYLA(configuracionaqua)
HF = interfazdemodulos.configurarhartreefock(operadores["operadorqubit"], configuracionaqua, propiedadesmolecula)
UCCSD = interfazdemodulos.configurarUCCSD(operadores["operadorqubit"], configuracionaqua, propiedadesmolecula, HF)
VQE = interfazdemodulos.configurarVQE(operadores["operadorqubit"], UCCSD, cobyla)

# Paso 4: Configurar la ejecucion
results = VQE.run()
print('The computed ground state energy is: {:.12f}'.format(results['eigvals'][0]))
print('The total ground state energy is: {:.12f}'.format(results['eigvals'][0] + operadores["energy_shift"] +
                                                         propiedadesmolecula["energia_de_repulsion_nuclear"]))
print("Parameters: {}".format(results['opt_params']))
