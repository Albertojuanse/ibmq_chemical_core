"""Esta clase crea un gestor de las conexiones con las máquinas cuánticas de IBM y los simuladores de Quiskit"""

# importa módulos
import qiskit
import time

# Variables globales
credencialescargadas = False
servidorescargados = False
servidoresreales = []
servidoressimuladores = []
servidor = None


def cargar_credenciales(interfazdeusuario=None):
    """Esta función auxiliar permite cargar las credenciales y establecer la conexión con IBMQ"""
    global credencialescargadas
    while not credencialescargadas:
        try:
            qiskit.IBMQ.load_accounts()
            credencialescargadas = True
        except:
            time.sleep(0.5)

        if interfazdeusuario:
            interfazdeusuario.mostrar_credenciales(credencialescargadas)


def cargar_servidores():
    """Esta función sondea a que servidores se tiene acceso y devuelve el resultado"""
    global credencialescargadas
    global servidoresreales
    global servidoressimuladores
    global servidor
    if not credencialescargadas:
        cargar_credenciales()

    while not servidorescargados:
        try:
            servidoresreales_simuladores = qiskit.IBMQ.backends()
            servidoressimuladores = qiskit.Aer.backends()
            servidoresreales = []
            for cada_servidor in servidoresreales_simuladores:
                if not cada_servidor.configuration()["simulator"] and cada_servidor.status()['operational']:
                    servidoresreales.append(cada_servidor)
            servidor = servidoressimuladores[0]
            servidoresreales_nombres, servidoressimuladores_nombres = [], []
            for cada_servidor in servidoresreales:
                servidoresreales_nombres.append(cada_servidor.configuration()["name"])
            for cada_servidor in servidoressimuladores:
                servidoressimuladores_nombres.append(cada_servidor.configuration()["name"])
            return servidoresreales_nombres, servidoressimuladores_nombres
        except:
            time.sleep(2)


def set_servidor(nombre_backend):
    """Esta función permite configurar un servidor en el que realizar la ejecución"""
    global servidoresreales
    global servidoressimuladores
    global servidor
    if not servidorescargados:
        cargar_servidores()
    for objeto_servidor in servidoresreales:
        if str(objeto_servidor.configuration()["name"]) == nombre_backend:
            servidor = objeto_servidor
            return True
    for objeto_servidor in servidoressimuladores:
        if str(objeto_servidor.configuration()["name"]) in servidoresreales:
            servidor = objeto_servidor
            return True
    return False


def get_servidor():
    """Esta función permite recuperar el servidor en el que realiza la ejecución"""
    global servidor
    return servidor.configuration()["name"]


def procesar_circuito(circuito, qubitsminimo=None):
    """Esta función recibe un circuito cuántico, lo trata, y devuelve los resultados"""
    global servidor
    if not servidor:
        cargar_servidores()
    if not servidor.status()['operational']:
        raise Exception("La maquina seleccionada para la ejecución está en mantenimiento; repita y escoja otra")

    if qubitsminimo:
        if not servidor.configuration()["simulator"] and int(servidor.configuration()['n_qubits']) >= qubitsminimo:
            raise Exception("La máquina elegida tiene menos cubits de los necesarios para desplegar el circuito")
    print(servidor)
    tarea = _enviar_circuito(circuito, servidor)
    resultados = _recibir_circuito(tarea, circuito)
    return resultados


def _enviar_circuito(circuito, backend):
    """Esta función envía un circuito al backend deseado"""
    return qiskit.execute(circuito, backend=backend, shots=1000)


def _recibir_circuito(tarea, circuito):
    """Esta función insiste en recolectar los resultados hasta que lo consigue"""
    while True:
        try:
            resultadocompleto = tarea.result(timeout=10)
            resultado = resultadocompleto.get_counts(circuito)
            return resultado
        except:
            time.sleep(5)
