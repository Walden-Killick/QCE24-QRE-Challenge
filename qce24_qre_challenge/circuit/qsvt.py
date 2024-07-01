"""Class for creating the QSVT circuit.

Cambridge Consultants 2024
Walden Killick
"""
from qce24_qre_challenge.circuit import BlockEncoding
from .circuit import Circuit


class QSVT(Circuit):
    def __init__(self, block_encoding: BlockEncoding, phase_angles: list[float]) -> None:
        self._block_encoding = block_encoding
        self._phase_angles = phase_angles
