"""Esta librería se ha importado de Qiskit Aqua y permite hacer ciertos cálculos físicos"""
# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================#

import logging
from pyscf import gto, scf, ao2mo
from pyscf.lib import param
from pyscf.lib import logger as pylogger
from qiskit_aqua_chemistry import AquaChemistryError
from qiskit_aqua_chemistry import QMolecule
import numpy as np

logger = logging.getLogger(__name__)


def compute_integrals(config):
    # Get config from input parameters
    # molecule is in PySCF atom string format e.g. "H .0 .0 .0; H .0 .0 0.2"
    #          or in Z-Matrix format e.g. "H; O 1 1.08; H 2 1.08 1 107.5"
    # other parameters are as per PySCF got.Mole format

    if 'atom' not in config:
        raise AquaChemistryError('Atom is missing')
    val = config['atom']
    if val is None:
        raise AquaChemistryError('Atom value is missing')

    atom = _check_molecule_format(val)
    basis = config.get('basis', 'sto3g')
    unit = config.get('unit', 'Angstrom')
    charge = int(config.get('charge', '0'))
    spin = int(config.get('spin', '0'))
    max_memory = config.get('max_memory')
    if max_memory is None:
        max_memory = param.MAX_MEMORY
    calc_type = config.get('calc_type', 'rhf').lower()

    try:
        mol = gto.Mole(atom=atom, unit=unit, basis=basis, max_memory=max_memory, verbose=pylogger.QUIET)
        mol.symmetry = False
        mol.charge = charge
        mol.spin = spin
        mol.build(parse_arg=False)
        ehf, enuke, norbs, mohij, mohijkl, mo_coeff, orbs_energy, x_dip, y_dip, z_dip, nucl_dip = _calculate_integrals(mol, calc_type)
    except Exception as exc:
        raise AquaChemistryError('Failed electronic structure computation') from exc

    # Create driver level molecule object and populate
    _q_ = QMolecule()
    # Energies and orbits
    _q_._hf_energy = ehf
    _q_._nuclear_repulsion_energy = enuke
    _q_._num_orbitals = norbs
    _q_._num_alpha = mol.nelec[0]
    _q_._num_beta = mol.nelec[1]
    _q_._mo_coeff = mo_coeff
    _q_._orbital_energies = orbs_energy
    # Molecule geometry
    _q_._molecular_charge = mol.charge
    _q_._multiplicity = mol.spin + 1
    _q_._num_atoms = mol.natm
    _q_._atom_symbol = []
    _q_._atom_xyz = np.empty([mol.natm, 3])
    atoms = mol.atom_coords()
    for _n in range(0, _q_._num_atoms):
        xyz = mol.atom_coord(_n)
        _q_._atom_symbol.append(mol.atom_pure_symbol(_n))
        _q_._atom_xyz[_n][0] = xyz[0]
        _q_._atom_xyz[_n][1] = xyz[1]
        _q_._atom_xyz[_n][2] = xyz[2]
    # 1 and 2 electron integrals. h1 & h2 are ready to pass to FermionicOperator
    _q_._mo_onee_ints = mohij
    _q_._mo_eri_ints = mohijkl
    # dipole integrals
    _q_._x_dip_mo_ints = x_dip
    _q_._y_dip_mo_ints = y_dip
    _q_._z_dip_mo_ints = z_dip
    # dipole moment
    _q_._nuclear_dipole_moment = nucl_dip
    _q_._reverse_dipole_sign = True

    return _q_


def _check_molecule_format(val):
    """If it seems to be zmatrix rather than xyz format we convert before returning"""
    atoms = [x.strip() for x in val.split(';')]
    if atoms is None or len(atoms) < 1:
        raise AquaChemistryError('Molecule format error: ' + val)

    # Anx xyz format has 4 parts in each atom, if not then do zmatrix convert
    parts = [x.strip() for x in atoms[0].split(' ')]
    if len(parts) != 4:
        try:
            return gto.mole.from_zmatrix(val)
        except Exception as exc:
            raise AquaChemistryError('Failed to convert atom string: ' + val) from exc

    return val


def _calculate_integrals(mol, calc_type='rhf'):
    """Function to calculate the one and two electron terms. Perform a Hartree-Fock calculation in
        the given basis.
    Args:
        mol : A PySCF gto.Mole object.
        calc_type: rhf, uhf, rohf
    Returns:
        ehf : Hartree-Fock energy
        enuke : Nuclear repulsion energy
        norbs : Number of orbitals
        mohij : One electron terms of the Hamiltonian.
        mohijkl : Two electron terms of the Hamiltonian.
        mo_coeff: Orbital coefficients
        orbs_energy: Orbitals energies
        x_dip_ints: x dipole moment integrals
        y_dip_ints: y dipole moment integrals
        z_dip_ints: z dipole moment integrals
        nucl_dipl : Nuclear dipole moment
    """
    enuke = gto.mole.energy_nuc(mol)

    if calc_type == 'rhf':
        mf = scf.RHF(mol)
    elif calc_type == 'rohf':
        mf = scf.ROHF(mol)
    elif calc_type == 'uhf':
        mf = scf.UHF(mol)
    else:
        raise AquaChemistryError('Invalid calc_type: {}'.format(calc_type))

    ehf = mf.kernel()

    if type(mf.mo_coeff) is tuple:
        mo_coeff = mf.mo_coeff[0]
        mo_occ   = mf.mo_occ[0]
    else:
        mo_coeff = mf.mo_coeff
        mo_occ   = mf.mo_occ

    norbs = mo_coeff.shape[0]
    orbs_energy = mf.mo_energy

    hij = mf.get_hcore()
    mohij = np.dot(np.dot(mo_coeff.T, hij), mo_coeff)

    eri = ao2mo.incore.full(mf._eri, mo_coeff, compact=False)
    mohijkl = eri.reshape(norbs, norbs, norbs, norbs)

    # dipole integrals
    mol.set_common_orig((0, 0, 0))
    ao_dip = mol.intor_symmetric('int1e_r', comp=3)
    x_dip_ints = QMolecule.oneeints2mo(ao_dip[0], mo_coeff)
    y_dip_ints = QMolecule.oneeints2mo(ao_dip[1], mo_coeff)
    z_dip_ints = QMolecule.oneeints2mo(ao_dip[2], mo_coeff)

    dm = mf.make_rdm1(mf.mo_coeff, mf.mo_occ)
    if calc_type == 'rohf' or calc_type == 'uhf':
        dm = dm[0]
    elec_dip = np.negative(np.einsum('xij,ji->x', ao_dip, dm).real)
    elec_dip = np.round(elec_dip, decimals=8)
    nucl_dip = np.einsum('i,ix->x', mol.atom_charges(), mol.atom_coords())
    nucl_dip = np.round(nucl_dip, decimals=8)
    logger.info("HF Electronic dipole moment: {}".format(elec_dip))
    logger.info("Nuclear dipole moment: {}".format(nucl_dip))
    logger.info("Total dipole moment: {}".format(nucl_dip+elec_dip))

    return ehf, enuke, norbs, mohij, mohijkl, mo_coeff, orbs_energy, x_dip_ints, y_dip_ints, z_dip_ints, nucl_dip
