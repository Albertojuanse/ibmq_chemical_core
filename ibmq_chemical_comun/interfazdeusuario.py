"""Esta clase implementa una interfaz de usuario y sus acciones"""

# Conexiones por arquitectura

# Dependencias

def __mostrar_mensaje_consola(mensaje):
    """Esta función imprime en la consola de usuario un mensaje"""
    print(mensaje)


def __hacer_pregunta(mensaje):
    """Esta función auxiliar permite hacer preguntas al usuario"""
    __mostrar_mensaje_consola("\n"+mensaje)
    while True:
        respuesta = input("Select [s/n]: ")
        if respuesta == "s" or respuesta == "si":
            return True
        if respuesta == "n" or respuesta == "no":
            return False


def __preguntar_opcion(mensaje, opciones):
    """Esta función pregunta al usuario para que elija una opción de una lista"""
    seleccion = "3"
    while seleccion not in [str(opciones.index(op)) for op in opciones]:
        __mostrar_mensaje_consola("\n"+mensaje)
        for i, op in enumerate(opciones):
            __mostrar_mensaje_consola(str(i) + ". -> " + str(op))

        seleccion = str(input("Seleccione una de las opciones " +
                              str([opciones.index(op) for op in opciones]) + ":")).lower()

        for i, op in enumerate(opciones):
            if seleccion == str(i):
                return op


def __preguntar_respuesta_abierta(mensaje):
    """Esta función auxiliar hace preguntas al usuario"""
    return input("\n"+mensaje).lower()


def bienvenida():
    """Esta función muestra por pantalla un mensaje de bienvenida"""
    __mostrar_mensaje_consola("Bienvenido a ibmq_chemical")
    
    
def preguntar_configuracion():
    """Esta función pregunta al usuario si desea usar la configuración del JSON o desea teclear una"""
    opciones = ["Mediante un archivo JSON", "Mediante línea de comandos"]
    respuesta = __preguntar_opcion("Por favor, indique como desea configurar la molécula:", opciones)
    if respuesta == "Mediante el archivo JSON":
        return None
    elif respuesta == "Mediante línea de comandos":
        configuracionmolecula = {'driver': 'PYSCF',
                               'configuracion': {
                                   'properties': {
                                       'atom': 'Li .0 .0 .0; H .0 .0 1.6',
                                       'unit': 'Angstrom',
                                       'charge': 0,
                                       'spin': 0,
                                       'basis': 'sto3g'}
                                    }
                               }
        # Validar con PySCF
        configuracionmolecula["configuracion"]["properties"]["atom"] =\
            __preguntar_respuesta_abierta("Introduce una estructura molecular válida:")
        haycarga = __hacer_pregunta("¿Tiene la molécula carga neta?")
        if haycarga:
            configuracionmolecula["configuracion"]["properties"]["charge"] =\
                __preguntar_respuesta_abierta("Introduzca el valor de la carga neta")
        haycarga = __hacer_pregunta("¿Tiene la molécula spin neto?")
        if haycarga:
            configuracionmolecula["configuracion"]["properties"]["spin"] =\
                __preguntar_respuesta_abierta("Introduzca el valor del spin neto")
        return configuracionmolecula


def mostrar_credenciales(credendialescargadas):
    """Esta función premite informar al usuario del proceso de carga de las credenciales de IBMQ"""
    __mostrar_mensaje_consola("Cargando servidores cuánticos disponibles...")
    if credendialescargadas:
        __mostrar_mensaje_consola("Se ha establecido conexión con IBMQ")
    else:
        __mostrar_mensaje_consola("Ha fallado la conexión con IBMQ\nSe reintentará en 3 segundos")


def mostrar_excepcion(excepcion):
    """Esta función muestra por pantalla una excepción"""
    __mostrar_mensaje_consola("[ERROR FATAL]: " + str(excepcion))


def mostrar_resultados(resultados, propiedadesmolecula, operadores):
    """Esta función da formato a los resultados que se obtienen y los muestra por pantalla"""
    __mostrar_mensaje_consola('The computed ground state energy is: {:.12f}'.format(resultados['eigvals'][0]))
    __mostrar_mensaje_consola('The total ground state energy is: {:.12f}'.format(resultados['eigvals'][0] +
                                operadores["energy_shift"] + propiedadesmolecula["energia_de_repulsion_nuclear"]))
    __mostrar_mensaje_consola("Parameters: {}".format(resultados['opt_params']))


def preguntar_terminar():
    """Esta funcion pregunta al usuario si desea salir del programa o repetir el cálculo"""
    while True:
        __mostrar_mensaje_consola("Desea realizar otro cálculo")
        respuesta = str(input("Seleccione [s/n]:")).lower()
        if respuesta == "s" or "si":
            return False
        elif respuesta == "n":
            __mostrar_mensaje_consola("Gracias por haber usado este programa")
            return True


def mostrar_informe_supervisor(supervisor, evento):
    """Esta función muestra un mensaje de un supervisor por pantalla"""
    __mostrar_mensaje_consola("[{}]: ".format(supervisor.nombre)+evento.contenido["mensaje"])
