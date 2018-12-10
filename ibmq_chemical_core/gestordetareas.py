# Conexiones por arquitectura

class GestorDeTareas():
    """Esta clase implementa un gestor de tareas con el fin de soptimizar las llamadas al gestor trasero"""

    def __init__(self):
        #Determina los servidores disponibles
        self.servidoresReales = GestorTrasero.getservidoresreales()
        self.servidoresSimuladores = GestorTrasero.getservidoressimuladores()
