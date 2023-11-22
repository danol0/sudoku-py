import numpy as np


class SudokuBoard:
    """
    @brief Class representing a sudoku board.
    """

    def __init__(self, initial_state: np.ndarray) -> None:
        """
        @brief Initializes the board with the specified initial state.

        The state of the board is sored as a 9x9 numpy array, where each cell contains the value of the cell.
        The possible values for each cell are stored in a 9x9 numpy array of sets, where each set contains the
        possible values for the corresponding cell.
        """
        if not isinstance(initial_state, np.ndarray):
            raise ValueError(
                "Trying to initialize board with an object that is not a numpy array."
            )
        if initial_state.shape != (9, 9):
            raise ValueError(
                "Trying to initialize board with an array of incorrect shape."
            )
        if (
            initial_state.dtype != int
            or np.any(initial_state < 0)
            or np.any(initial_state > 9)
        ):
            raise ValueError(
                "Trying to initialize board with an array containing invalid values."
            )

        # TODO: Check that the initial state is valid.

        self.state = initial_state
        p_vals = np.array([set(range(1, 10)) for _ in range(81)])
        self.possible_values = p_vals.reshape(9, 9)
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
        @brief Updates the possible values given the current state of the board.
        """
        for i in range(9):
            for j in range(9):
                if self.state[i, j] == 0:
                    self.possible_values[i, j] -= set(
                        self.related_cells(self.state, (i, j))
                    )
                if self.state[i, j] != 0:
                    self.possible_values[i, j] = set()

    def propigate_constraints(self) -> bool:
        """
        @brief Iteratively updates the state of the board for cells with only one possible value.
        """
        state_updated = True
        while state_updated:
            if np.all(self.state != 0):
                return True

            self.update_possible_values()
            state_updated = False

            for i in range(9):
                for j in range(9):
                    if len(self.possible_values[i, j]) == 1:
                        self.state[i, j] = self.possible_values[i, j].pop()
                        state_updated = True
        return False

    def related_cells(self, grid: np.ndarray, index: tuple) -> np.ndarray:
        """
        @brief Returns the contents of all cells that are related to the specified index.
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
        @brief Attempts to solve the board by applying constraint propigation.
        """
        if self.propigate_constraints():
            print("The board was solved by constraint propigation.")
            return True
        else:
            print("The board could not be solved by constraint propigation.")
            return False
