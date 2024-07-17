"""Classes for constructing quantum oracles for accessing sparse matrices.

Cambridge Consultants 2024
Walden Killick
"""

from qce24_qre_challenge.quantum_oracle.banded_circulant_oracle import (
    BandedCirculantOracle,
)
from qce24_qre_challenge.quantum_oracle.sparse_oracle import SparseOracle

__all__ = ["SparseOracle", "BandedCirculantOracle"]
