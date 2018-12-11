# https://mail.python.org/pipermail/python-es/2004-March/004155.html
import weakref
import time
from threading import Thread, Lock


class Supervisor(Thread):
    """Esta clase crea un supervisor para un determinado tipo de evento"""

    def __init__(self, nombre, interfazdeusuario=None):
        Thread.__init__(self)
        self.nombre = nombre
        self.evento_reportado = False
        self.eventos = []
        self.contenidoevento = {}
        self.cerrojo = Lock()
        if interfazdeusuario:
            self.interfazdeusuario = interfazdeusuario

    def run(self):
        """Esta función se ejecuta mientras el supervisor esté vivo"""
        while True:
            if self.evento_reportado:
                try:
                    self.cerrojo.acquire()
                    for evento in self.eventos:
                        self.en_evento(evento)
                        self.eventos.remove(evento)
                    self.evento_reportado = False
                finally:
                    self.cerrojo.release()
            time.sleep(1)

    def reportar_evento(self, evento):
        """Esta función permite a un evento reportarse"""
        self.eventos.append(evento)
        self.evento_reportado = True

    def en_evento(self, evento):
        """Esta función define el comportamiento del supervisor ante un evento"""
        contenido = evento.getcontenido()
        if self.interfazdeusuario:
            self.interfazdeusuario.mostrar_informe_supervisor(self, evento)
        else:
            print("[{}]: ".format(self.nombre) + contenido["mensaje"])


class Evento:
    """Esta clase define un evento o interrupción del programa"""
    def __init__(self, nombre, supervisores=None):
        self.nombre = nombre
        # Cada evento tiene asociado una lista de supervisores a los que anunciarse
        self.supervisores = []
        self.contenido = {
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
        if isinstance(supervisor,Supervisor):
            if supervisor in self.supervisores:
                self.supervisores.remove(weakref.ref(supervisor))
        # pero si es un listado de ellos
        elif isinstance(supervisor, (list,tuple)):
            for cadasupervisor in supervisor:
                if isinstance(cadasupervisor,Supervisor):
                    self.supervisores.remove(weakref.ref(supervisor))

    def dar_de_baja_todos(self):
        """Este método elimina del registro de reporte a los supervisores; el evento ya no se anunciará ante ninguno"""
        self.supervisores = []

    def anunciarse(self, contenido):
        """Con esta función se reporta a sus supervisores"""
        self.contenido = contenido
        for supervisor in self.supervisores:
            ref = supervisor()  # weakref handle
            if ref:
                ref.reportar_evento(self)

    def getcontenido(self):
        """Devuelve el contenido del evento"""
        return self.contenido
