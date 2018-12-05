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
    if gestortrasero.cargar_servidores():
        credendialescargadas = True
    else:
        time.sleep(3)
    interfazdeusuario.mostrar_credenciales(credendialescargadas)

# Lectura del los archivos de configuración del problema
configuracionmolecula = interfazdeusuario.preguntar_configuracion()
if configuracionmolecula is None:
    configuracionmolecula = interfazsistema.importar_propiedades("properties", "molecula.json")
configuracionaqua = interfazsistema.importar_propiedades("properties", "problema.json")

# Paso 1: cálculo de la molécula
molecula = interfazdemodulos.procesar_molecula(configuracionmolecula)

# Paso 2: preparar el hamiltoniano
propiedadesmolecula = interfazdemodulos.leer_propiedades_molecula(molecula)
operadores = interfazdemodulos.obtener_operadores_hamiltonianos(propiedadesmolecula, configuracionaqua)
interfazdemodulos.calcular_energia_clasico(propiedadesmolecula, operadores["operadorqubit"], operadores["energy_shift"])

# Paso 3: Configurar problema y cargar de Aqua los algoritmos
cobyla = interfazdemodulos.configurar_COBYLA(configuracionaqua)
HF = interfazdemodulos.configurar_hartreefock(operadores["operadorqubit"], configuracionaqua, propiedadesmolecula)
UCCSD = interfazdemodulos.configurar_UCCSD(operadores["operadorqubit"], configuracionaqua, propiedadesmolecula, HF)
VQE = interfazdemodulos.configurar_VQE(operadores["operadorqubit"], UCCSD, cobyla)

# Paso 4: Configurar la ejecucion
resultados = VQE.run()
interfazdeusuario.mostrar_resultados(resultados, propiedadesmolecula, operadores)
