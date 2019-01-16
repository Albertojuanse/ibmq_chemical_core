"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
from ibmq_chemical_comun import interfazdeusuario, interfazsistema
from ibmq_chemical_core import gestortrasero, interfazdemodulos

# Dependencias
import time
from dependencies.eventos import SupervisorDeResultados,  SupervisorDeResultadosParaAPI
import numpy

# Variables globales
listaservidoresreales = []
listaservidoressimuladores = []
servidor = None


def obtener_backends():
    """Esta función devuelve los objetos de los servidores disponibles"""
    # Se cargan las credenciales
    gestortrasero.cargar_credenciales()
    global listaservidoresreales
    global listaservidoressimuladores
    global servidor
    listaservidoresreales, listaservidoressimuladores = gestortrasero.cargar_servidores()
    servidor = gestortrasero.get_servidor()
    return listaservidoresreales, listaservidoressimuladores, servidor


def configurar_backend(nombre_backend):
    """Esta función configura un servidor de los disponibles"""
    gestortrasero.set_servidor(nombre_backend)


def get_backend():
    """Esta función recupera del gestor trasero el servidor configurado"""
    return gestortrasero.get_servidor()


def set_backend(nombre):
    """Esta función configura en el gestor trasero el servidor"""
    return gestortrasero.set_servidor(nombre)


def ejecutar_ibmq_vqe(configuracionproblema=None,
                      configuracionmolecula=None,
                      interfazdeusuario_local=False,
                      dibujo=None,
                      backend='statevector_simulator'):
    """Lanza la ejecución principal del programa"""

    if interfazdeusuario_local:
        # MODO LÍNEA DE COMANDOS
        interfazdeusuario.bienvenida()
        # Se despiertan a los supervisores necesarios
        supervisorderesultados = SupervisorDeResultados("supervisor de resultados",
                                                        interfazdeusuario=interfazdeusuario)
        # Lectura del los archivos de configuración del problema
        configuracionmolecula = interfazdeusuario.preguntar_configuracion()
    else:
        # MODO API
        # Se despiertan a los supervisores necesarios
        supervisorderesultados = SupervisorDeResultadosParaAPI("supervisor de resultados para API")

    if not configuracionmolecula:
        configuracionmolecula = interfazsistema.importar_propiedades("properties", "molecula.json")
    if not configuracionproblema:
        configuracionproblema = interfazsistema.importar_propiedades("properties", "problema.json")

    def lanzar_vqe(barrido=None):
        # Paso 1: cálculo de la molécula
        molecula = interfazdemodulos.procesar_molecula(configuracionmolecula, barrido)

        # Paso 2: preparar el hamiltoniano
        propiedadesmolecula = interfazdemodulos.leer_propiedades_molecula(molecula, supervisorderesultados)
        operadores = interfazdemodulos.obtener_operadores_hamiltonianos(propiedadesmolecula, configuracionproblema)
        interfazdemodulos.calcular_energia_clasico(propiedadesmolecula,
                                                   operadores["operadorqubit"],
                                                   operadores["energy_shift"],
                                                   supervisorderesultados
                                                   )

        # Paso 3: Configurar problema y cargar de Aqua los algoritmos
        cobyla = interfazdemodulos.configurar_COBYLA(configuracionproblema)
        HF = interfazdemodulos.configurar_hartreefock(operadores["operadorqubit"],
                                                      configuracionproblema,
                                                      propiedadesmolecula
                                                      )
        UCCSD = interfazdemodulos.configurar_UCCSD(operadores["operadorqubit"],
                                                   configuracionproblema,
                                                   propiedadesmolecula,
                                                   HF
                                                   )
        VQE = interfazdemodulos.configurar_VQE(operadores["operadorqubit"], UCCSD, cobyla, backend)
        resultado = VQE.run()["energy"]
        if interfazdeusuario_local:
            interfazdeusuario.mostrar_resultados(resultado, propiedadesmolecula, operadores)
        else:
            consola = supervisorderesultados.get_consola()
            supervisorderesultados.borrar_consola()
            return resultado, consola

    if not dibujo:
        distancias = None
        energia, consolas = lanzar_vqe()
    else:
        distancias = numpy.arange(0.5, 5.5, 0.1)
        consolas = []
        energia = numpy.zeros(1, len(distancias))
        for i, distancia in enumerate(distancias):
            energia[i], consolas[i] = lanzar_vqe(distancia)
    return energia, consolas, distancias


def ejecutar_numero_aleatorio(cifras=5, servidor=None):
    """Esta función permite calcular un número aleatorio"""
    # Se compone el circuito basado en Qiskit
    circuito = interfazdemodulos.circuito_numeros_aleatorios(cifras)
    if servidor:
        set_backend(servidor)
    # Se envía el circuito para su ejecución
    resultados = gestortrasero.procesar_circuito(circuito, cifras).items()
    # Se procesa el resultado
    mayori, mayorj = 0, 0
    for i, j in resultados:
        if int(j) > int(mayorj):
            mayori = i
            mayorj = j
    print(mayori, mayorj)
    return mayori
