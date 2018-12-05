# https://mail.python.org/pipermail/python-es/2004-March/004155.html
import weakref


class Supervisor:
    """Esta clase crea un supervisor para un determinado tipo de evento"""
    def __init__(self, nombre):
        self.nombre = nombre

    @classmethod
    def en_evento(cls, evento):
        print("El supervisor {} ha capturado el evento {}".format(self.nombre, evento.nombre))


class Evento:
    """Esta clase define un evento o interrupción del programa"""
    def __init__(self, nombre, supervisores = None):
        self.nombre = nombre
        # Cada evento tiene asociado una lista de supervisores a los que anunciarse
        self.supervisores = []
        if supervisores:
            self.registro(supervisores)

    @classmethod
    def registro(cls, supervisor):
        """Este método añade supervisores al listado de reporte; el evento se anunciará a los supervisores registrados"""
        #quitamos morralla (referencias inválidas) (mantengo comentario original)
        cls.supervisores = [l for l in cls.supervisores if l() != None]

        # Si el parametro es un solo supervisor
        if isinstance(supervisor,Supervisor):
            cls.supervisores.append(weakref.ref(supervisor))
        # pero si es un listado de ellos
        elif isinstance(supervisor, (list,tuple)):
            for cadasupervisor in supervisor:
                if isinstance(cadasupervisor,Supervisor):
                    cls.supervisores.append(weakref.ref(supervisor))

    @classmethod
    def dar_de_baja(cls, supervisor):
        """Este método elimina del registro de reporte a un supervisor concreto; el evento ya no se anunciará ante él"""
        # Si el parametro es un solo supervisor
        if isinstance(supervisor,Supervisor):
            if supervisor in cls.supervisores:
                cls.supervisores.remove(weakref.ref(supervisor))
        # pero si es un listado de ellos
        elif isinstance(supervisor, (list,tuple)):
            for cadasupervisor in supervisor:
                if isinstance(cadasupervisor,Supervisor):
                    cls.supervisores.remove(weakref.ref(supervisor))

    @classmethod
    def dar_de_baja_todos(cls):
        """Este método elimina del registro de reporte a los supervisores; el evento ya no se anunciará ante ninguno"""
        cls.supervisores = []

    @classmethod
    def anunciarse(cls):
        for supervisor in cls.supervisores:
            ref = supervisor()  # weakref handle
            if ref:
                ref.en_evento(cls)
