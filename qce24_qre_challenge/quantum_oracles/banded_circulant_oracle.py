"""Class for banded circulant quantum oracles.

Cambridge Consultants 2024
Walden Killick
"""
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.gate import Gate
from qiskit.circuit.library.standard_gates import XGate, RYGate
from qce24_qre_challenge.quantum_oracles import SparseOracle
from qce24_qre_challenge.sparse_matrices import BandedCirculantMatrix
import numpy as np


def loc_shift_gate(num_qubits: int, direction: str) -> Gate:
    """Function to create quantum gates for a left or right index shift.

    Parameters
    ----------
    num_qubits : int
        Number of qubits.
    direction : str
        Whether to create a left-shift ('l') or right-shift ('r') gate.

    Returns
    -------
    Gate
        Quantum gate for the shift circuit.

    Raises
    ------
    NameError
        If the direction argument is not 'l' or 'r'.
    """
    if direction == 'l':
        ctrl_state = '1'
        name = 'L'
    elif direction == 'r':
        ctrl_state = '0'
        name = 'R'
    else:
        raise NameError(f"Direction variable ('{direction}') must be either 'l' or 'r'.")
    
    shift_circuit = QuantumCircuit(num_qubits)
    for i in reversed(range(1, num_qubits)):
        ncx_gate = XGate().control(i, ctrl_state=ctrl_state*i)
        shift_circuit.append(ncx_gate, range(i+1))
    shift_circuit.x(0)
    shift_gate = shift_circuit.to_gate()
    shift_gate.name = name
    return shift_gate


class BandedCirculantOracle(SparseOracle):
    """Class for creating sparse-access oracles."""
    def __init__(self, banded_circulant_matrix: BandedCirculantMatrix) -> None:
        self._banded_circulant_matrix = banded_circulant_matrix

    def location_oracle(self) -> QuantumCircuit:
        """Construct the quantum oracle which locates the non-zero matrix entries.

        Returns
        -------
        QuantumCircuit
            Quantum oracle O_c.
        """
        matrix_size = self._banded_circulant_matrix._size
        loc_reg_num_qubits = int(np.ceil(np.log2(matrix_size)))

        c_l_shift_gate = loc_shift_gate(loc_reg_num_qubits, 'l').control(1)
        c_r_shift_gate = loc_shift_gate(loc_reg_num_qubits, 'r').control(1)

        control_reg = QuantumRegister(2)
        output_reg = QuantumRegister(loc_reg_num_qubits)

        loc_oracle_circuit = QuantumCircuit(control_reg, output_reg)
        loc_oracle_circuit.append(c_l_shift_gate, [0] + list(range(2, loc_reg_num_qubits + 2)))
        loc_oracle_circuit.append(c_r_shift_gate, [1] + list(range(2, loc_reg_num_qubits + 2)))

        return loc_oracle_circuit

    def value_oracle(self) -> QuantumCircuit:
        """Construct the quantum oracle which computes the matrix entry values.

        Returns
        -------
        QuantumCircuit
            Quantum oracle O_A.
        """
        coefficients = self._banded_circulant_matrix.get_coefficients()
        alpha = coefficients[1]
        beta = coefficients[0]
        gamma = coefficients[2]

        theta_0 = 2*np.arccos(alpha - 1)
        theta_1 = 2*np.arccos(beta)
        theta_2 = 2*np.arccos(gamma)

        c_theta_0 = RYGate(theta_0).control(2, ctrl_state='00')
        c_theta_1 = RYGate(theta_1).control(2, ctrl_state='01')
        c_theta_2 = RYGate(theta_2).control(2, ctrl_state='10')

        value_reg = QuantumRegister(1)
        control_reg = QuantumRegister(2)

        val_oracle_circuit = QuantumCircuit(value_reg, control_reg)
        val_oracle_circuit.append(c_theta_0, [1,2,0])
        val_oracle_circuit.append(c_theta_1, [1,2,0])
        val_oracle_circuit.append(c_theta_2, [1,2,0])

        return val_oracle_circuit