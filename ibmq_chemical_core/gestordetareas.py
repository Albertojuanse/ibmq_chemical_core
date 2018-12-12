# Conexiones por arquitectura
from ibmq_chemical_core import gestortrasero, orquestador


class GestorDeTareas:
    """Esta clase implementa un gestor de tareas con el fin de soptimizar las llamadas al gestor trasero"""

    def __init__(self):
        # Determina los servidores disponibles
        self.servidoresReales = gestortrasero.getservidoresreales()
        self.servidoresSimuladores = gestortrasero.getservidoressimuladores()
