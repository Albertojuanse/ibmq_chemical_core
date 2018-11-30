"""Esta clase servirá de enlace entre Quiskit, drivers... y el cliente"""

# Dependencias comunes
from collections import OrderedDict

# Dependencias de aqua
from qiskit_aqua_chemistry.drivers import ConfigurationManager


def procesarmolecula(configuraciondriver):
    gestorconfiguracion = ConfigurationManager()
    driver = gestorconfiguracion.get_driver_instance(configuraciondriver["driver"])
    return driver.run(configuraciondriver["configuracion"])
