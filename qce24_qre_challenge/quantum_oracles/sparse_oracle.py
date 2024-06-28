"""Base class for sparse quantum oracles.

Cambridge Consultants 2024
Walden Killick
"""
from abc import ABC, abstractmethod
from qiskit import QuantumCircuit


class SparseOracle(ABC):

    @abstractmethod
    def location_oracle(self) -> QuantumCircuit:
        pass

    @abstractmethod
    def value_oracle(self) -> QuantumCircuit:
        pass