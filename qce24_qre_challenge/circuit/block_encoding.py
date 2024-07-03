"""Class to create block-encoding circuits from sparse access oracles.

Cambridge Consultants 2024
Walden Killick
"""

from qiskit import QuantumCircuit, QuantumRegister
from qce24_qre_challenge.quantum_oracle import SparseOracle
from .circuit import Circuit


class BlockEncoding(Circuit):
    """Class for creating block-encoding circuits from sparse-access oracles."""

    def __init__(self, sparse_oracle: SparseOracle) -> None:
        """Initialise the 'BlockEncoding'.

        Parameters
        ----------
        sparse_oracle : SparseOracle
            Sparse-access oracles to construct the block encoding from.
        """
        self._location_oracle = sparse_oracle.location_oracle()
        self._value_oracle = sparse_oracle.value_oracle()

    def create_circuit(self) -> QuantumCircuit:
        """Create the block-encoding circuit.

        Returns
        -------
        QuantumCircuit
            Quantum circuit which block-encodes the matrix defined by the sparse-access
            oracles.
        """
        control_reg_size = self._value_oracle.num_qubits - 1
        output_reg_size = self._location_oracle.num_qubits - control_reg_size

        value_reg = QuantumRegister(1, name="val")
        control_reg = QuantumRegister(control_reg_size, name="ctrl")
        output_reg = QuantumRegister(output_reg_size, name="out")

        block_encoding_circuit = QuantumCircuit(value_reg, control_reg, output_reg)

        block_encoding_circuit.h(control_reg)
        block_encoding_circuit.compose(
            self._value_oracle, qubits=range(control_reg_size + 1), inplace=True
        )
        block_encoding_circuit.compose(
            self._location_oracle,
            qubits=range(1, control_reg_size + output_reg_size + 1),
            inplace=True,
        )
        block_encoding_circuit.h(control_reg)

        return block_encoding_circuit

    @property
    def num_qubits(self) -> int:
        """Get the total number of qubits used in constructing the block encoding.

        Returns
        -------
        int
            Number of qubits.
        """
        return self._location_oracle.num_qubits + 1

    @property
    def num_ancillas(self) -> int:
        """Get the number of ancilla qubits used in constructing the block encoding.

        Returns
        -------
        int
            Number of ancillas.
        """
        return self._value_oracle.num_qubits
