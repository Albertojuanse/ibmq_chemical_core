"""Esta clase crea un gestor de las conexiones con las máquinas cuánticas de IBM y los simuladores de Quiskit"""

# importa módulos
import qiskit
import time


def cargar_credenciales(interfazdeusuario=None):
    """Esta función auxiliar permite cargar las credenciales y establecer la conexión con IBMQ"""
    credendialescargadas = False
    while not credendialescargadas:
        try:
            qiskit.IBMQ.load_accounts()
            credendialescargadas = True
        except:
            time.sleep(1)

        if interfazdeusuario:
            interfazdeusuario.mostrar_credenciales(credendialescargadas)


def cargar_servidores():
    """Esta función sondea a que servidores se tiene acceso"""
    try:
        servidoresreales = qiskit.IBMQ.backends()
        servidoressimuladores = qiskit.Aer.backends()
        return servidoresreales, servidoressimuladores
    except:
        time.sleep(5)


def get_servidores_reales(servidoresreales):
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
    # Se precisa eliminar los simuladores de esta lista
    listaservidoresreales = []
    for servidor in servidoresreales:
        if not servidor.configuration()["simulator"] and servidor.status()['operational']:
            listaservidoresreales.append(servidor)
    return listaservidoresreales


def get_servidores_simuladores(servidoressimuladores):
    """Esta función devuelve un listado con los servidores reales disponibles en linea"""
    return servidoressimuladores


def procesar_circuito(circuito, backend, qubitsminimo=None):
    """Esta función recibe un circuito cuántico, lo trata, y devuelve los resultados"""
    if not backend.status()['operational']:
        raise Exception("La maquina seleccionada para la ejecución está en mantenimiento; repita y escoja otra")

    if qubitsminimo:
        if int(backend.configuration()['n_qubits']) >= qubitsminimo:
            raise Exception("La máquina elegida tiene menos cubits de los necesarios para desplegar el circuito")

    tarea = _enviar_circuito(circuito, backend)
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
            if ('status' not in resultadocompleto.keys()):
                resultado = resultadocompleto.get_counts(circuito)
                return resultado
        except:
            time.sleep(5)
