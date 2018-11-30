"""Esta clase implementa una interfaz de usuario y sus acciones"""

# Conexiones por arquitectura

# Dependencias


def __mostrarmensajeconsola(mensaje):
    """Esta función imprime en la consola de usuario un mensaje"""
    print(mensaje)


def bienvenida():
    __mostrarmensajeconsola("Bienvenido a ibmq_chemical_core")


def mostrarcredenciales(credendialescargadas):
    __mostrarmensajeconsola("Cargando servidores cuánticos disponibles...")
    if credendialescargadas:
        __mostrarmensajeconsola("Se ha establecido conexión con IBMQ")
    else:
        __mostrarmensajeconsola("Ha fallado la conexión con IBMQ\nSe reintentará en 3 segundos")

def mostrarexcepcion(excepcion):
    __mostrarmensajeconsola("[ERROR FATAL]: " + str(excepcion))


def mostrarresultados():
    pass
