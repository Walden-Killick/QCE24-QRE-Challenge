"""Base class for sparse matrices.

Cambridge Consultants 2024
Walden Killick
"""
from abc import ABC, abstractmethod


class SparseMatrix(ABC):
    """Base class for sparse matrices."""

    @abstractmethod
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
        """
        pass

    @abstractmethod
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
        pass
