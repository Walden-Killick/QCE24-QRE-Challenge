"""Base class for sparse quantum oracles.

Cambridge Consultants 2024
Walden Killick
"""

from abc import ABC, abstractmethod

from qiskit import QuantumCircuit


class SparseOracle(ABC):
    """Base class for sparse access oracles."""

    @abstractmethod
    def location_oracle(self) -> QuantumCircuit:
        """Construct the quantum oracle which locates the non-zero matrix entries.

        Returns
        -------
        QuantumCircuit
            Quantum oracle O_c.
        """
        pass

    @abstractmethod
    def value_oracle(self) -> QuantumCircuit:
        """Construct the quantum oracle which computes the matrix entry values.

        Returns
        -------
        QuantumCircuit
            Quantum oracle O_A.
        """
        pass
