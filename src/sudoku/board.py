import numpy as np
import time
import warnings


class sudokuBoard:
    """
    Class representing a Sudoku board.

    Parameters
    ----------
    initial_state : numpy.ndarray[int]
        The initial state of the board.

    Attributes
    ----------
    state : numpy.ndarray[int]
        The current state of the board.

    possible_values : numpy.ndarray[set]
        The possible values for each cell.

    indices : list[tuple[int, int]]
        The indices of each cell.

    Raises
    ------
    ValueError :
        If the initial state is not a 9x9 numpy array or contains invalid values.

    Returns
    -------
    self : object
        Initialized SudokuBoard object.
    """

    def __init__(self, initial_state: np.ndarray) -> None:
        """
        Initializes the board object from the specified initial state.
        """
        # check that the initial state is valid
        if not isinstance(initial_state, np.ndarray):
            raise ValueError(
                "Trying to initialize board with an object that is not an array."
            )
        if initial_state.dtype != np.int64:
            raise ValueError(
                "Trying to initialize board with an array of incorrect dtype."
            )
        if initial_state.shape != (9, 9):
            try:
                initial_state = initial_state.reshape(9, 9)
            except ValueError:
                raise ValueError(
                    "Trying to initialize board with an array of incorrect shape."
                )
        if np.logical_or(initial_state < 0, initial_state > 9).any():
            raise ValueError(
                "Trying to initialize board with an array containing invalid values."
            )

        # initialize indices and state attributes
        self.indices = [(i, j) for i in range(9) for j in range(9)]
        self.state = initial_state

        if np.count_nonzero(self.state) < 17:
            warnings.warn("WARNING: The puzzle has multiple solutions.")

        # initialize the possible values attribute & update
        values_set = np.array([set(range(1, 10)) for _ in range(81)])
        self.possible_values = values_set.reshape(9, 9)
        self.update_possible_values()

    def __str__(self) -> str:
        """
        Prints the board state in a readable format.

        Returns
        -------
        output : str
            A string representation of the board.

        Examples
        --------
        >>> print(board)
        594|167|832
        618|239|574
        237|458|169
        ---+---+---
        981|726|345
        375|841|296
        426|395|781
        ---+---+---
        762|584|913
        143|972|658
        859|613|427
        """
        output = ""
        for row in range(9):
            if row == 3 or row == 6:
                output += "---+---+---\n"
            for col in range(9):
                if col == 3 or col == 6:
                    output += "|"
                output += str(self.state[row, col])
            output += "\n"
        return output

    def solve(self) -> bool:
        """
        Attempts to solve the board by calling constraint propagation and then backtracking.

        Returns
        -------
        solved : bool
            True if the board was solved, False if no solutions exist.

        Raises
        ------
        ValueError
            If no solutions exist for the puzzle. The search time is included in the error message.
        """
        start = time.time()

        if self.propagate_constraints():
            end = time.time()
            print(
                f"The puzzle was solved by constraint propagation in {end - start:.3} seconds."
            )
            return True

        elif self.backtrack(self.state):
            end = time.time()
            print(f"The puzzle was solved by brute force in {end - start:.3} seconds")
            return True

        else:
            end = time.time()
            raise ValueError(
                f"No solutions exist for this puzzle. Search took {end - start:.3} seconds."
            )

    def update_possible_values(self) -> None:
        """
        Updates the possible values attribute given the current state of the board.
        """
        # for empty cells, remove values in related cells from the possible values
        for index in self.indices:
            if self.state[index] == 0:
                self.possible_values[index] -= self.related_cells(self.state, (index))

                # if no possible values, the board is invalid
                if self.possible_values[index] == set():
                    raise ValueError("No solutions exist for this puzzle.")

    def related_cells(self, grid: np.ndarray, index: tuple) -> set:
        """
        Returns the contents of all cells in the given grid that are related to the specified index.

        Note
        ----
        Related cells are those in the same row, column, or box as the given cell.
        The returned set includes the contents of the given cell.

        Parameters
        ----------
        grid : numpy.ndarray
            The grid to search.

        index : tuple
            The index of the cell to find related cells for.

        Returns
        -------
        related : set
            The set of values in all related cells.
        """
        row, col = index
        # calculate the index of the top left cell in the box containing the given cell
        box_row = row // 3 * 3
        box_col = col // 3 * 3

        related = {
            *grid[row, :],
            *grid[:, col],
            *grid[box_row : box_row + 3, box_col : box_col + 3].flatten(),
        }

        return related

    def propagate_constraints(self) -> bool:
        """
        Assigns values for cells with only one possible value and propagates.

        Note
        ----
        Assignment is to the state attribute.
        Propagation continues until no more updates are made or the board is full.

        Returns
        -------
        solved : bool
            True if the board is complete, False otherwise.
        """
        # if board is full, return
        if np.all(self.state):
            return True

        # update possible values for the current state
        self.update_possible_values()

        for index in self.indices:
            # if cell has only one possible value, assign it and propagate
            if len(self.possible_values[index]) == 1:
                self.state[index] = self.possible_values[index].pop()
                return self.propagate_constraints()

        # return False once propagation is complete
        return False

    def backtrack(self, grid: np.ndarray) -> bool:
        """
        Recursive, depth-first search on the given board state.

        Note
        ----
        If a solution is found, the state attribute is updated to the solved board.

        Args
        ----
        grid : numpy.ndarray
            The board state to search.

        Returns
        -------
        solved : bool
            True if a solution was found, False otherwise.
        """
        # base case: if board is full, return
        if np.all(grid):
            self.state = grid
            return True

        # this implements the least possible values heuristic - see section 3.3.2 of report
        # find the index of the cell with the least possible values
        least_possible_values_index = np.argmax(
            [
                len(self.related_cells(grid, index)) if grid[index] == 0 else 0
                for index in self.indices
            ]
        )
        # pass this index to the backtrack search
        index = self.indices[least_possible_values_index]

        # only try values that are still possible given the current state of the board
        for value in self.possible_values[index] - self.related_cells(grid, index):
            # assign the value and recurse
            grid[index] = value
            if self.backtrack(grid):
                return True

            # if no solution found, reset the cell and try the next value
            grid[index] = 0

        # return False if all values have been tried without finding a solution
        return False
