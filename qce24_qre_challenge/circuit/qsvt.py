"""Class for creating the QSVT circuit.

Cambridge Consultants 2024
Walden Killick
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
from qiskit.circuit.library.standard_gates import XGate
from qiskit.quantum_info import Statevector

from qce24_qre_challenge.circuit import BlockEncoding

from .circuit import Circuit


def signal_processing_circuit(angle: float, num_ancillas: int) -> QuantumCircuit:
    """Create the signal-processing circuit (projector-controlled rotation).

    Parameters
    ----------
    angle : float
        Phase angle.
    num_ancillas : int
        Number of ancillas used in the block encoding.

    Returns
    -------
    QuantumCircuit
        Phase gate controlled by ancillas in the all-zero state. As described in
        https://doi.org/10.1145/3313276.3316366.
    """
    circuit = QuantumCircuit(num_ancillas + 1)
    n0x_gate = XGate().control(num_ancillas, ctrl_state=0)
    circuit.append(n0x_gate, reversed(range(num_ancillas + 1)))
    circuit.rz(2 * angle, 0)
    circuit.append(n0x_gate, reversed(range(num_ancillas + 1)))
    return circuit


class QSVT(Circuit):
    """Class for creating QSVT circuits."""

    def __init__(
        self,
        block_encoding: BlockEncoding,
        phase_angles: list[float],
        initial_state: np.ndarray = None,
    ) -> None:
        """Initialise the 'QSVT'.

        Parameters
        ----------
        block_encoding : BlockEncoding
            Block encoding circuit to apply the transformation to.
        phase_angles : list[float]
            Phase angles determining the polynomial transformation.
        initial_state : np.ndarray, optional
            Initial state to prepare in the output register.
        """
        self._block_encoding = block_encoding
        self._phase_angles = phase_angles
        self._initial_state = initial_state

    def create_circuit(self) -> QuantumCircuit:
        """Create the QSVT circuit.

        Returns
        -------
        QuantumCircuit
            Circuit which block-encodes a polynomial transformation of the input matrix.
        """
        total_qubits = self._block_encoding.num_qubits + 1
        num_ancillas = self._block_encoding.num_ancillas

        block_encoding_circuit = self._block_encoding.create_circuit()
        block_encoding_gate = block_encoding_circuit.to_gate()
        block_encoding_gate.name = "U_A"

        processing_reg = QuantumRegister(1, name="rot")
        ancilla_reg = QuantumRegister(num_ancillas, name="anc")
        output_reg = QuantumRegister(total_qubits - num_ancillas - 1, name="out")

        qsvt_circuit = QuantumCircuit(processing_reg, ancilla_reg, output_reg)

        if self._initial_state is not None:
            state_prep_gate = StatePreparation(
                params=Statevector(self._initial_state), label="Load b"
            )
            qsvt_circuit.append(state_prep_gate, output_reg)

        qsvt_circuit.h(processing_reg)

        for angle in self._phase_angles[:-1]:
            qsvt_circuit.compose(
                signal_processing_circuit(angle, num_ancillas), inplace=True
            )
            qsvt_circuit.append(block_encoding_gate, range(1, total_qubits))
        qsvt_circuit.compose(
            signal_processing_circuit(self._phase_angles[-1], num_ancillas),
            inplace=True,
        )

        qsvt_circuit.h(0)

        return qsvt_circuit
