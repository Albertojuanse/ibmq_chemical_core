from ibmq_chemical_core import orquestador
from dependencies.eventos import Supervisor
from ibmq_chemical_comun import interfazdeusuario


# Se despiertan a los supervisores necesarios
class SupervisorDeResultados(Supervisor):
    """Supervisor de resultados para el usuario"""

    def en_evento(self, evento):
        """Comportamiento del supervisor ante un evento"""
        interfazdeusuario.mostrar_informe_supervisor(self, evento)
