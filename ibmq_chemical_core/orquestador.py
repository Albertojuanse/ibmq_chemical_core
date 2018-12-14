"""Esta clase ejecuta el hilo principal del cliente"""

# Conexiones por arquitectura
from ibmq_chemical_comun import interfazdeusuario, interfazsistema
from ibmq_chemical_core import gestortrasero, interfazdemodulos

# Dependencias
import time
from dependencies.eventos import SupervisorDeResultados,  SupervisorDeResultadosParaAPI


def obtener_backends():
    """Esta función devuelve los objetos de los servidores disponibles"""
    # Se cargan las credenciales
    gestortrasero.cargar_credenciales()
    servidoresreales, servidoressimuladores = gestortrasero.cargar_servidores()
    listaservidoresreales = gestortrasero.get_servidores_reales(servidoresreales)
    listaservidoressimuladores = gestortrasero.get_servidores_simuladores(servidoressimuladores)
    return listaservidoresreales, listaservidoressimuladores


def ejecutar_ibmq_vqe(configuracionproblema=None, configuracionmolecula=None):
    """Lanza la ejecución principal del programa"""

    if not configuracionmolecula and configuracionproblema:
        raise Exception("Debe proporcionar dos parámetros, no solo uno")

    elif configuracionmolecula and not configuracionproblema:
        raise Exception("Debe proporcionar dos parámetros, no solo uno")

    elif not configuracionmolecula and not configuracionproblema:
        # MODO LÍNEA DE COMANDOS
        interfazdeusuario.bienvenida()

        # Se despiertan a los supervisores necesarios
        supervisorderesultados = SupervisorDeResultados("supervisor de resultados", interfazdeusuario=interfazdeusuario)

        # Lectura del los archivos de configuración del problema
        configuracionmolecula = interfazdeusuario.preguntar_configuracion()
        if not configuracionmolecula:
            configuracionmolecula = interfazsistema.importar_propiedades("properties", "molecula.json")
        configuracionproblema = interfazsistema.importar_propiedades("properties", "problema.json")

        # Paso 1: cálculo de la molécula
        molecula = interfazdemodulos.procesar_molecula(configuracionmolecula)

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
        VQE = interfazdemodulos.configurar_VQE(operadores["operadorqubit"], UCCSD, cobyla)

        # Paso 4: Configurar la ejecucion
        resultados = VQE.run()
        interfazdeusuario.mostrar_resultados(resultados, propiedadesmolecula, operadores)

    elif configuracionmolecula and configuracionproblema:
        # MODO API

        # Se despiertan a los supervisores necesarios
        supervisorderesultados = SupervisorDeResultadosParaAPI("supervisor de resultados para API")

        # Paso 1: cálculo de la molécula
        molecula = interfazdemodulos.procesar_molecula(configuracionmolecula)

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
        VQE = interfazdemodulos.configurar_VQE(operadores["operadorqubit"], UCCSD, cobyla)

        # Paso 4: Configurar la ejecucion
        resultados = VQE.run()["energy"]
        consola = supervisorderesultados.get_consola()

        return resultados, consola


def ejecutar_numero_aleatorio(cifras=None, backend=None):
    """Esta función permite calcular un número aleatorio"""
    # Se compone el circuito basado en Qiskit
    circuito = interfazdemodulos.circuito_numeros_aleatorios(cifras)
    # Se envía el circuito para su ejecución
    resultados = gestortrasero.procesar_circuito(circuito, backend, cifras).item()
    # Se procesa el resultado
    mayori, mayorj = 0
    for i, j in resultados:
        if int(j) > int(mayorj):
            mayori = i
            mayorj = j
    print(mayori, mayorj)
    return mayori
