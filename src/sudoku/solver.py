from .board import sudokuBoard
import numpy as np
import time


class sudokuSolver(sudokuBoard):
    """
    This class defines a solver object with methods for solving Sudoku puzzles.

    Parameters
    ----------
    initial_state : str or numpy.ndarray[int] or list[list[int]]
        The initial state of the board.

    Methods
    -------
    solve()
        Attempts to solve the board by calling constraint propagation and then backtracking.

    propagate_constraints()
        Assigns values for cells with only one possible value and propagates.

    backtrack(grid)
        Recursive, depth-first search on the given board state.

    See Also
    --------
    sudokuBoard :
        Parent class of sudokuSolver that contains methods for initializing boards.

    Examples
    --------
    Initialise and solve a board:

    >>> board = sudokuSolver("input.txt")
    Loading initial state from file: input.txt
    >>> board.solve()
    The puzzle was solved by constraint propagation in 0.002 seconds.
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
    859|613|472

    A value error is raised if no solutions exist:

    >>> board = sudokuSolver("invalid.txt")
    Loading initial state from file: invalid.txt
    >>> board.solve()
    ValueError: No solutions exist for this puzzle. Search took 0.002 seconds.
    """

    def __init__(self, initial_state: str | np.ndarray | list[list[int]]) -> None:
        super().__init__(initial_state)

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
            # if backtracking fails, no solutions exist
            end = time.time()
            raise ValueError(
                f"No solutions exist for this puzzle. Search took {end - start:.3} seconds."
            )

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

        # this implements the least possible values heuristic - see section 3.3.2 report
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
