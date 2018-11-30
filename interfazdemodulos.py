"""Esta clase servirá de enlace entre Quiskit, drivers... y el cliente"""

# Dependencias comunes
from collections import OrderedDict

# Dependencias de aqua
from qiskit_aqua_chemistry.drivers import ConfigurationManager
from qiskit_aqua_chemistry import FermionicOperator
from qiskit_aqua import (get_algorithm_instance, get_optimizer_instance,
                          get_variational_form_instance, get_initial_state_instance)


def procesarmolecula(configuraciondriver):
    gestorconfiguracion = ConfigurationManager()
    driver = gestorconfiguracion.get_driver_instance(configuraciondriver["driver"])
    return driver.run(configuraciondriver["configuracion"])


def leerpropiedadesmolecula(molecula):
    propiedadesmolecula = {}
    propiedadesmolecula["h1"] = molecula._one_body_integrals
    propiedadesmolecula["h2"] = molecula._two_body_integrals
    propiedadesmolecula["energia_de_repulsion_nuclear"] = molecula._nuclear_repulsion_energy
    propiedadesmolecula["numero_de_particulas"] = molecula._num_alpha + molecula._num_beta
    propiedadesmolecula["numero_de_orbitales"] = molecula._num_orbitals
    propiedadesmolecula["numero_de_orbitales_de_spin"] = molecula._num_orbitals * 2
    propiedadesmolecula["energia_HF"] = molecula._hf_energy
    print("Energía con el método Hartree-Fock: {}".format(propiedadesmolecula["energia_HF"] - propiedadesmolecula["energia_de_repulsion_nuclear"]))
    print("# de electrones: {}".format(propiedadesmolecula["numero_de_particulas"]))
    print("# de orbitales de spin: {}".format(propiedadesmolecula["numero_de_orbitales_de_spin"]))
    return propiedadesmolecula


def __obteneroperadorfermionico(h1, h2):
    return FermionicOperator(h1=h1, h2=h2)


def __reductordeorbitales(propiedadesmolecula, operadorfermionico):
    energy_shift = 0.0
    # please be aware that the idx here with respective to original idx
    freeze_list = [0]
    remove_list = [-3, -2]  # negative number denotes the reverse order

    # prepare full idx of freeze_list and remove_list
    # convert all negative idx to positive
    remove_list = [x % propiedadesmolecula["numero_de_orbitales"] for x in remove_list]
    freeze_list = [x % propiedadesmolecula["numero_de_orbitales"] for x in freeze_list]
    # update the idx in remove_list of the idx after frozen, since the idx of orbitals are changed after freezing
    remove_list = [x - len(freeze_list) for x in remove_list]
    remove_list += [x + propiedadesmolecula["numero_de_orbitales"] - len(freeze_list) for x in remove_list]
    freeze_list += [x + propiedadesmolecula["numero_de_orbitales"] for x in freeze_list]

    # prepare fermionic hamiltonian with orbital freezing and eliminating, and then map to qubit hamiltonian
    # and if PARITY mapping is selected, reduction qubits

    if len(freeze_list) > 0:
        operadorfermionico, energy_shift = operadorfermionico.fermion_mode_freezing(freeze_list)
        propiedadesmolecula["numero_de_orbitales_de_spin"] -= len(freeze_list)
        propiedadesmolecula["numero_de_particulas"] -= len(freeze_list)
    if len(remove_list) > 0:
        operadorfermionico = operadorfermionico.fermion_mode_elimination(remove_list)
        propiedadesmolecula["numero_de_orbitales_de_spin"] -= len(remove_list)

    return operadorfermionico, energy_shift


def __necesariareduccion(tipo_de_mapeo):
    return True if tipo_de_mapeo == "parity" else False


def __obteneroperadorqbit(propiedadesmolecula, configuracionaqua, operadorfermionico):
    operadorqubit = operadorfermionico.mapping(map_type=configuracionaqua["general"]["tipo_de_mapeo"], threshold=0.00000001)
    operadorqubit = operadorqubit.two_qubit_reduced_operator(
        propiedadesmolecula["numero_de_particulas"]) if __necesariareduccion(configuracionaqua["general"]["tipo_de_mapeo"]) else operadorqubit
    operadorqubit.chop(10**-10)
    return operadorqubit


def obteneroperadoreshamiltonianos(propiedadesmolecula, configuracionaqua):
    operadorfermionico = __obteneroperadorfermionico(propiedadesmolecula["h1"], propiedadesmolecula["h2"])
    operadorfermionico, energy_shift = __reductordeorbitales(propiedadesmolecula, operadorfermionico)
    operadorqubit = __obteneroperadorqbit(propiedadesmolecula, configuracionaqua, operadorfermionico)
    return {"operadorfermionico": operadorfermionico, "energy_shift": energy_shift, "operadorqubit": operadorqubit}


def calcularenergiaclasico(propiedadesmolecula, operadorqubit, energy_shift):
    """Esta función usa obtiene la energía de enlace menor mediante el cálculo del menor autovalor del sistema"""
    exact_eigensolver = get_algorithm_instance('ExactEigensolver')
    exact_eigensolver.init_args(operadorqubit, k=1)
    ret = exact_eigensolver.run()
    print('The computed energy is: {:.12f}'.format(ret['eigvals'][0].real))
    print('The total ground state energy is: {:.12f}'.format(ret['eigvals'][0].real + energy_shift +
                                                             propiedadesmolecula["energia_de_repulsion_nuclear"]))


def configurarCOBYLA(configuracionaqua):
    """Esta función obtiene una instancia del optimizador COBYLA configurada"""
    cobyla = get_optimizer_instance('COBYLA')
    cobyla.set_options(maxiter=configuracionaqua["COBYLA"]["max_eval"])
    return cobyla


def configurarhartreefock(operadorqubit, configuracionaqua, propiedadesmolecula):
    """Esta función obtiene una instancia configurada del método de aproximación de la función de onda Hartree-Fock"""
    HF = get_initial_state_instance('HartreeFock')
    HF.init_args(operadorqubit.num_qubits, propiedadesmolecula["numero_de_orbitales_de_spin"],
                 configuracionaqua["general"]["tipo_de_mapeo"], __necesariareduccion(configuracionaqua["general"]["tipo_de_mapeo"]),
                 propiedadesmolecula["numero_de_particulas"])
    return HF


def configurarUCCSD(operadorqubit, configuracionaqua, propiedadesmolecula, HF):
    """Esta función obtiene una instancia configurada del método numérico UCCSD"""
    UCCSD = get_variational_form_instance('UCCSD')
    UCCSD.init_args(operadorqubit.num_qubits, depth=configuracionaqua["UCCSD"]["profundidad"],
                       num_orbitals=propiedadesmolecula["numero_de_orbitales"],
                       num_particles=propiedadesmolecula["numero_de_particulas"],
                       active_occupied=configuracionaqua["UCCSD"]["orbitales_activos_ocupados"],
                       active_unoccupied=configuracionaqua["UCCSD"]["orbitales_activos_no_ocupados"],
                       initial_state=HF , qubit_mapping=configuracionaqua["general"]["tipo_de_mapeo"],
                       two_qubit_reduction=__necesariareduccion(configuracionaqua["general"]["tipo_de_mapeo"]),
                       num_time_slices=configuracionaqua["UCCSD"]["numero_de_slices"])
    return UCCSD


def configurarVQE(operadorqubit, UCCSD, cobyla):
    """Esta función obtiene una instancia configurada del algoritmo VQE"""
    VQE = get_algorithm_instance('VQE')
    VQE.setup_quantum_backend(backend='statevector_simulator')
    VQE.init_args(operadorqubit, 'matrix', UCCSD, cobyla)
    return VQE
