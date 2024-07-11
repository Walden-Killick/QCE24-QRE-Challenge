"""Class for creating the HHL circuit.

Cambridge Consultants 2024
Walden Killick
"""

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
from qiskit.circuit.library import QFT
import numpy as np
from qiskit.quantum_info import Statevector
from .circuit import Circuit


def qpe_circuit(
    clock_reg: QuantumRegister,
    output_reg: QuantumRegister,
    target_unitary: QuantumCircuit,
) -> QuantumCircuit:
    """Create the QPE circuit.

    Parameters
    ----------
    clock_reg : QuantumRegister
        Clock register. Size determines the accuracy of the output.
    output_reg : QuantumRegister
        Register which the target unitary acts upon.
    target_unitary : QuantumCircuit
        Unitary to perform phase estimation on.

    Returns
    -------
    QuantumCircuit
        Quantum phase estimation circuit.
    """
    circuit = QuantumCircuit(clock_reg, output_reg)

    circuit.h(clock_reg)

    for i in range(len(clock_reg)):
        indicies = [i] + list(
            range(len(clock_reg), len(clock_reg) + target_unitary.num_qubits)
        )
        u_n_gate = target_unitary.repeat(2**i).to_gate(label=f"U^{2**i}")
        ctrl_u_n_gate = u_n_gate.control()

        circuit.append(ctrl_u_n_gate, indicies)

    qft_gate = QFT(len(clock_reg)).to_gate()
    circuit.append(qft_gate.inverse(), clock_reg)

    return circuit


class HHL(Circuit):
    """Class for creating HHL circuits."""

    def __init__(
        self,
        clock_reg_num_qubits: int,
        target_unitary: QuantumCircuit,
        initial_state: np.ndarray = None,
    ) -> None:
        self._clock_reg_num_qubits = clock_reg_num_qubits
        self._target_unitary = target_unitary
        self._initial_state = initial_state

    def create_circuit(self) -> QuantumCircuit:
        """Create the HHL algorithm circuit.

        Currently not functional - the middle ancilla rotation step has not yet been
        implemented.

        Returns
        -------
        QuantumCircuit
            Circuit for the HHL algorithm.
        """
        ancilla_reg = QuantumRegister(1, name="anc")
        clock_reg = QuantumRegister(self._clock_reg_num_qubits, name="clock")
        output_reg = QuantumRegister(self._target_unitary.num_qubits, name="out")

        total_qubits = 1 + self._clock_reg_num_qubits + self._target_unitary.num_qubits

        hhl_circuit = QuantumCircuit(ancilla_reg, clock_reg, output_reg)
        if self._initial_state is not None:
            state_prep_gate = StatePreparation(
                params=Statevector(self._initial_state), label="Load b"
            )
            hhl_circuit.append(state_prep_gate, output_reg)

        qpe_gate = qpe_circuit(clock_reg, output_reg, self._target_unitary).to_gate()
        qpe_gate.name = "QPE"

        hhl_circuit.append(qpe_gate, range(total_qubits)[1:])

        # TODO: ancilla rotation step

        hhl_circuit.append(qpe_gate.inverse(), range(total_qubits)[1:])

        return hhl_circuit
