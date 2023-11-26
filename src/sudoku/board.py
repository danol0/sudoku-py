import numpy as np
import time


class SudokuBoard:
    """
    Class representing a Sudoku board.

    Attributes:
        state (numpy.ndarray): The current state of the board.

        possible_values (numpy.ndarray): The possible values for each cell, stored as an array of sets.

        indices (list[tuple[int, int]]): The indices of each cell on the board.

    Args:
        initial_state (numpy.ndarray): The initial state of the board.

    Raises:
        ValueError: If the initial state is not a 9x9 numpy array or contains invalid values.

    Returns:
        SudokuBoard: A new SudokuBoard object.
    """

    def __init__(self, initial_state: np.ndarray) -> None:
        """
        Initializes the board with the specified initial state.
        """
        if not isinstance(initial_state, np.ndarray):
            raise ValueError(
                "Trying to initialize board with an object that is not a numpy array."
            )
        if initial_state.shape != (9, 9):
            raise ValueError(
                "Trying to initialize board with an array of incorrect shape."
            )
        if np.logical_or(initial_state < 0, initial_state > 9).any():
            raise ValueError(
                "Trying to initialize board with an array containing invalid values."
            )

        # TODO: check that the initial state is valid
        self.indices = [(i, j) for i in range(9) for j in range(9)]
        self.state = initial_state
        self.possible_values = np.array([set(range(1, 10)) for _ in range(81)]).reshape(
            9, 9
        )
        self.update_possible_values()

    def __str__(self) -> str:
        """
        Prints the board state in a readble format.

        Returns:
            str: A string representation of the board state.
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

    def update_possible_values(self) -> None:
        """
        Updates the possible values given the current state of the board.
        """
        for index in self.indices:
            if self.state[index] == 0:
                self.possible_values[index] -= set(
                    self.related_cells(self.state, (index))
                )

    def propagate_constraints(self) -> bool:
        """
        Assigns numbers to cells with only one possible value and propagates.

        Returns:
            bool: True if the board is solved, False otherwise.
        """
        # if board is full, return
        if np.all(self.state != 0):
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

    def related_cells(self, grid: np.ndarray, index: tuple) -> np.ndarray:
        """
        Returns the contents of all cells in the given grid that are related to the specified index.

        Note:
            Related cells are those in the same row, column, or box as the given cell.
            The returned array includes the contents of the given cell.

        Args:
            grid (numpy.ndarray): The grid to search.
            index (tuple): The index of the cell to find related cells for.

        Returns:
            numpy.ndarray: A 1D array containing the contents of all related cells.
        """
        row, col = index
        # find the index of the top-left cell of the box
        b_row, b_col = row - row % 3, col - col % 3
        related = (
            grid[row, :],
            grid[:, col],
            grid[b_row : (b_row + 3), b_col : (b_col + 3)].flatten(),
        )
        return np.concatenate(related)

    def solve(self) -> bool:
        """
        Attempts to solve the board by applying constraint propagation and then backtracking.

        Returns:
            bool: True if the board was solved, False otherwise.
        """
        start = time.time()
        if self.propagate_constraints():
            end = time.time()
            print(
                f"The board was solved by constraint propagation in {end - start:.3} seconds."
            )
            return True
        elif self.backtrack(self.state):
            end = time.time()
            print(f"The board was solved by brute force in {end - start:.3} seconds")
            return True
        else:
            end = time.time()
            print(f"No solutions exist. Search took {end - start:.3} seconds.")
            return False

    def backtrack(self, grid: np.ndarray) -> bool:
        """
        Recursive, depth-first search on the given board state.

        Note:
            If a solution is found, the state of the SudokuBoard object is updated to the solved board.

        Args:
            grid (numpy.ndarray): The board state to search.

        Returns:
            bool: True if a solution was found, False otherwise.
        """
        # if board is full, return
        if np.all(grid != 0):
            self.state = grid
            return True

        # find next empty cell
        index = np.where(grid == 0)[0][0], np.where(grid == 0)[1][0]

        # try each possible value
        for value in self.possible_values[index]:
            # if valid, assign the value
            if value not in self.related_cells(grid, (index)):
                grid[index] = value

                # repeat search with the new grid
                if self.backtrack(grid):
                    return True

            # if no valid value, reset the cell and try the next value
            grid[index] = 0

        # return False when branch is exhausted
        return False
