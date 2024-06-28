"""Class for banded circulant quantum oracles.

Cambridge Consultants 2024
Walden Killick
"""
from quantum_oracles import SparseOracle
from sparse_matrices import BandedCirculantMatrix


class BandedCirculantOracle(SparseOracle):
    def __init__(self, banded_circulant_matrix: BandedCirculantMatrix) -> None:
        self._banded_circulant_matrix = banded_circulant_matrix
    