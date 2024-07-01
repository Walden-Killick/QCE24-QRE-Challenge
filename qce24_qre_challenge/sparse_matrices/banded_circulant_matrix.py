"""Class for banded circulant matrices.

Cambridge Consultants 2024
Walden Killick
"""
from qce24_qre_challenge.sparse_matrices import SparseMatrix


class BandedCirculantMatrix(SparseMatrix):
    """Class for banded circulant matrices.

    For a definition of banded circulant matrices, see 
    https://doi.org/10.1137/22M1484298.
    """
    def __init__(self, size: int, coefficients: list[float]) -> None:
        """Initialise the 'BandedCirculantMatrix'.

        Parameters
        ----------
        size : int
            Dimension (number of columns) of the matrix.
        coefficients : list[float]
            The three coefficients defining the subdiagonal, diagonal, and superdiagonal
            matrix elements, respectively.

        Raises
        ------
        ValueError
            If the number of coefficients given is not exactly three.
        """
        if len(coefficients) != 3:
            raise ValueError("The number of coefficients to initialise a banded circulant " + 
                             f"matrix must be exactly 3. {len(coefficients)} were given.")
        self._size = size
        self._coefficients = coefficients
        self._sparsity = 3

    @property
    def coefficients(self) -> list[float]:
        """Return the coefficients defining the banded circulant matrix.

        Returns
        -------
        list[float]
            The three coefficients defining the subdiagonal, diagonal, and superdiagonal
            matrix elements, respectively.
        """
        return self._coefficients

    def get_entry_location(self, nonzero_entry_index: int, column_index: int) -> int:
        """Oracle for locating the nonzero matrix entries.

        Parameters
        ----------
        nonzero_entry_index : int
            Index to specify which nonzero entry to locate in a given column.
        column_index : int
            Index to specify which column to locate the nonzero entry in.

        Returns
        -------
        int
            Row index specifying where the nonzero entry is.

        Raises
        ------
        ValueError
            If the nonzero entry index is out of bounds.
        """
        if not 0 <= nonzero_entry_index <= self._sparsity - 1:
            raise ValueError(f"Nonzero entry index ({nonzero_entry_index}) out of bounds " + 
                             f"(must lie between 0 and {self._sparsity - 1}.)")

        return (column_index + nonzero_entry_index - 1) % self._size

    def get_entry_value(self, row_index: int, column_index: int) -> float:
        """Oracle for querying the matrix entries.

        Parameters
        ----------
        row_index : int
            Row index.
        column_index : int
            Column Index.

        Returns
        -------
        float
            The value of the matrix entry at the given row and column indicies.
        """
        offset = ((row_index - column_index + 1) % self._size) - 1

        if -1 <= offset <= 1:
            return self._coefficients[offset + 1]
        return 0