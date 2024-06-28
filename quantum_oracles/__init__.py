"""Classes for constructing quantum oracles for accessing sparse matrices.

Cambridge Consultants 2024
Walden Killick
"""
from quantum_oracles.sparse_oracle import SparseOracle
from quantum_oracles.banded_circulant_oracle import BandedCirculantOracle

__all__ = ["SparseOracle", "BandedCirculantOracle"]