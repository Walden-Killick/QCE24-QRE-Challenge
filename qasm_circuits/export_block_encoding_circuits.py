"""Script for exporting block encoding circuits as QASM text files.

Cambridge Consultants 2024\
Walden Killick
"""

from pathlib import Path

from qiskit import qasm2

from qce24_qre_challenge.circuit import BlockEncoding
from qce24_qre_challenge.quantum_oracle import BandedCirculantOracle
from qce24_qre_challenge.sparse_matrix import BandedCirculantMatrix

MATRIX_SIZES = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

for matrix_size in MATRIX_SIZES:
    print(f"Creating circuit for matrix size {matrix_size}...")

    # Creating a random banded circulant matrix and its block-encoding circuit
    matrix = BandedCirculantMatrix(size=matrix_size)
    banded_circulant_oracle = BandedCirculantOracle(matrix)
    block_encoding = BlockEncoding(banded_circulant_oracle)
    block_encoding_circuit = block_encoding.create_circuit()
    qasm_circuit = qasm2.dumps(block_encoding_circuit)

    filepath = str(Path(__file__).resolve().parent)
    filename = f"block_encoding_{matrix_size}"

    with open(filepath + "/block_encoding_circuits/" + filename, "w") as file:
        file.write(qasm_circuit)
