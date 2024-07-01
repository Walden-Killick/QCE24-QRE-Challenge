"""Base class for classes which generate quantum circuits.

Cambridge Consultants 2024
Walden Killick
"""
from abc import ABC, abstractmethod
from qiskit import QuantumCircuit


class Circuit(ABC):
    """Base class for quantum circuit classes"""
    @abstractmethod
    def create_circuit() -> QuantumCircuit:
        """Create the relevant 'QuantumCircuit'.

        Returns
        -------
        QuantumCircuit
            Quantum circuit.
        """
        pass