"""Esta librería contiene las clases necesarias para la gestión de eventos"""
# https://mail.python.org/pipermail/python-es/2004-March/004155.html
import weakref


class Supervisor:
    """Esta clase crea un supervisor para un determinado tipo de evento"""

    def __init__(self, nombre, interfazdeusuario=None):
        self.nombre = nombre
        self.coladeeventos = []
        self.contenidoevento = {}
        if interfazdeusuario:
            self.interfazdeusuario = interfazdeusuario

    def en_evento(self, evento):
        """Esta función define el comportamiento del supervisor"""
        contenido = evento.getcontenido()
        if self.interfazdeusuario:
            self.interfazdeusuario.mostrar_informe_supervisor(self, evento)
        else:
            print("[{}]: ".format(self.nombre) + contenido["mensaje"])


class SupervisorDeResultados(Supervisor):
    """Supervisor de resultados para el usuario"""

    def en_evento(self, evento):
        """Comportamiento del supervisor ante un evento"""
        self.interfazdeusuario.mostrar_informe_supervisor(self, evento)


class Evento:
    """Esta clase define un evento o interrupción del programa"""
    def __init__(self, nombre, supervisores=None):
        self.nombre = nombre
        # Cada evento tiene asociado una lista de supervisores a los que anunciarse
        self.supervisores = []
        self._contenido = {
            "mensaje": "Este evento no tiene mensaje de contenido"
        }
        if supervisores:
            self.registro(supervisores)

    def registro(self, supervisor):
        """Este método añade supervisores al listado de reporte; el evento se anunciará a los supervisores
         registrados"""
        # quitamos morralla (referencias inválidas) (mantengo comentario original)
        self.supervisores = [l for l in self.supervisores if l() != None]

        # Si el parametro es un solo supervisor
        if isinstance(supervisor, Supervisor):
            self.supervisores.append(weakref.ref(supervisor))
        # pero si es un listado de ellos
        elif isinstance(supervisor, (list, tuple)):
            for cadasupervisor in supervisor:
                if isinstance(cadasupervisor, Supervisor):
                    self.supervisores.append(weakref.ref(supervisor))

    def dar_de_baja(self, supervisor):
        """Este método elimina del registro de reporte a un supervisor concreto; el evento ya no se anunciará ante él"""
        # Si el parametro es un solo supervisor
        if isinstance(supervisor, Supervisor):
            if supervisor in self.supervisores:
                self.supervisores.remove(weakref.ref(supervisor))
        # pero si es un listado de ellos
        elif isinstance(supervisor, (list, tuple)):
            for cadasupervisor in supervisor:
                if isinstance(cadasupervisor, Supervisor):
                    self.supervisores.remove(weakref.ref(supervisor))

    def dar_de_baja_todos(self):
        """Este método elimina del registro de reporte a los supervisores; el evento ya no se anunciará ante ninguno"""
        self.supervisores = []

    def anunciarse(self, contenido):
        """Con esta función se reporta a sus supervisores"""
        self._contenido = contenido
        for supervisor in self.supervisores:
            ref = supervisor()  # weakref handle
            if ref:
                ref.en_evento(self)

    def getcontenido(self):
        """Devuelve el contenido del evento"""
        return self._contenido
