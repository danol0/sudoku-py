import numpy as np


class SudokuBoard:
    """
    @brief Class representing a sudoku board.
    """

    def __init__(self, initial_state: np.ndarray) -> None:
        """
        @brief Initializes the board with the specified initial state.

        The state of the board is stored as a 9x9 numpy array.
        The possible values for each cell are stored in a 9x9 numpy array of sets.

        @param initial_state: The initial state of the board.
        @type initial_state: numpy.ndarray
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
        @brief Prints the board state in the format specified by the instructions.
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
        @brief Updates the matrix of possible values given the current state of the board.
        """
        for index in self.indices:
            if self.state[index] == 0:
                self.possible_values[index] -= set(
                    self.related_cells(self.state, (index))
                )

    def propagate_constraints(self) -> bool:
        """
        @brief Recursively updates the state of the board for cells with only one possible value.
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
        @brief Returns the contents of all cells in the given grid that are related to the specified index.
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

    def solve(self) -> None:
        """
        @brief Attempts to solve the board by applying constraint propigation, and then backtracking.
        """
        if self.propagate_constraints():
            print("The board was solved by constraint propigation.")
            return True
        elif self.backtrack(self.state):
            print("The board was solved through brute force.")
            return True
        else:
            print("It was not possible to solve the puzzle.")
            return False

    def backtrack(self, grid: np.ndarray) -> bool:
        """
        @brief Recursive, depth first search on the given board state.
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
