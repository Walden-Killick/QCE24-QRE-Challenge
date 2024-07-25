"""Script for exporting QSVT circuits as QASM text files.

Cambridge Consultants 2024\
Walden Killick
"""

from pathlib import Path

import numpy as np
import pyqsp
from pyqsp.angle_sequence import Polynomial
from qiskit import qasm2

from qce24_qre_challenge.circuit import QSVT, BlockEncoding
from qce24_qre_challenge.quantum_oracle import BandedCirculantOracle
from qce24_qre_challenge.sparse_matrix import BandedCirculantMatrix

MATRIX_SIZES = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
KAPPA = 3
EPSILON = 0.1

# Creating the polynomial which approximates 1/x.
pg = pyqsp.poly.PolyOneOverX()
pcoefs = pg.generate(kappa=KAPPA, epsilon=EPSILON)
poly = Polynomial(pcoefs)
sequence_length = len(poly)

# Finding the phase angles for QSVT is quite involved and the pyqsp subroutine may fail
# for high-degree polynomials. However, the single-qubit rotation angles should make
# no difference to resource estimates and thus for this purpose it will be sufficient
# to replace the true phase angles with a random sequence of the same length.
ang_seq = np.random.rand(sequence_length) * np.pi

for matrix_size in MATRIX_SIZES:
    print(f"Creating circuit for matrix size {matrix_size}...")

    # Creating a random banded circulant matrix and its block-encoding circuit
    matrix = BandedCirculantMatrix(size=matrix_size)
    banded_circulant_oracle = BandedCirculantOracle(matrix)
    block_encoding = BlockEncoding(banded_circulant_oracle)

    # Creating the QSVT circuit from the block encoding and outputting to a QASM string.
    qsvt = QSVT(block_encoding, ang_seq)
    qsvt_circuit = qsvt.create_circuit()
    qasm_circuit = qasm2.dumps(qsvt_circuit)

    filepath = str(Path(__file__).resolve().parent)
    filename = f"qsvt_{matrix_size}_{EPSILON}"

    with open(filepath + "/qsvt_circuits/" + filename, "w") as file:
        file.write(qasm_circuit)
