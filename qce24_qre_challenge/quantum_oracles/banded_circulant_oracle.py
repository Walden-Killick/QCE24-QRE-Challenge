"""Class for banded circulant quantum oracles.

Cambridge Consultants 2024
Walden Killick
"""
from qiskit import QuantumCircuit
from qce24_qre_challenge.quantum_oracles import SparseOracle
from qce24_qre_challenge.sparse_matrices import BandedCirculantMatrix


class BandedCirculantOracle(SparseOracle):
    def __init__(self, banded_circulant_matrix: BandedCirculantMatrix) -> None:
        self._banded_circulant_matrix = banded_circulant_matrix
    def location_oracle(self) -> QuantumCircuit:
        return super().location_oracle()
    def value_oracle(self) -> QuantumCircuit:
        return super().value_oracle()