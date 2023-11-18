import numpy as np


class SudokuBoard:
    """
    @brief Class representing the state of a sudoku board.
    """

    def __init__(self, initial_state: np.ndarray) -> None:
        """
        @brief Initializes the board with the specified initial state.

        The state of the board is sored as a 9x9 numpy array, where each cell contains the value of the cell.
        The possible values for each cell are stored in a 9x9 numpy array of sets, where each set contains the
        possible values for the corresponding cell.
        """
        if not isinstance(initial_state, np.ndarray):
            raise ValueError("Trying to initialize board with an object that is not a numpy array.")
        if initial_state.shape != (9, 9):
            raise ValueError("Trying to initialize board with an array of incorrect shape.")
        if initial_state.dtype != int or np.any(initial_state < 0) or np.any(initial_state > 9):
            raise ValueError("Trying to initialize board with an array containing invalid values.")

        self.state = initial_state
        self.possible_values = self.initialise_possible_values(self.state)

    def initialise_possible_values(self, state: np.ndarray) -> np.ndarray:
        """
        @brief Initializes the possible values for each cell in the board given the initial state.
        """
        possible_values = np.array([set(range(1, 10)) for _ in range(81)]).reshape(9, 9)
        for row in range(9):
            for col in range(9):
                if state[row, col] != 0:
                    possible_values[row, col] = set([state[row, col]])
        return possible_values

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

    def get_row(self, row: int) -> np.ndarray:
        """
        @brief Returns the row at the specified index.
        """
        return self.state[row, :]

    def get_col(self, col: int) -> np.ndarray:
        """
        @brief Returns the column at the specified index.
        """
        return self.state[:, col]

    def get_box(self, box: tuple) -> np.ndarray:
        """
        @brief Returns the box that the specified index belongs to.
        """
        row, col = box
        # find the index of the top-left cell of the box
        row = row - row % 3
        col = col - col % 3
        return self.state[row:(row + 3), col:(col + 3)].flatten()

    def related_cells(self, cell: tuple) -> np.ndarray:
        """
        @brief Returns all cells that are related to the specified cell.
        """
        row, col = cell
        return np.concatenate((self.get_row(row), self.get_col(col), self.get_box((row, col))))

    def update_possible_values(self) -> None:
        """
        @brief Updates the possible values given the current state of the board.
        """
        for i in range(9):
            for j in range(9):
                if self.state[i, j] == 0:
                    self.possible_values[i, j] -= set(self.related_cells((i, j)))

    def apply_pencil_mark_constraint(self) -> bool:
        """
        @brief Updates the state of the board for cells with only one possible value.
        """
        state_updated = False
        for i in range(9):
            for j in range(9):
                if len(self.possible_values[i, j]) == 1:
                    self.state[i, j] = self.possible_values[i, j].pop()
                    state_updated = True
        return state_updated

    def propigate_constraints(self) -> None:
        """
        @brief Recursively applies the constraints until no updates are made or the board is solved.
        """
        self.update_possible_values()

        if np.all(self.state != 0):
            print("The puzzle has been solved.")
            return True

        if self.apply_pencil_mark_constraint() is False:
            print("It was not possible to solve the puzzle using constraint propigation.")
            return False

        else:
            self.propigate_constraints()

# TODO: will update this function to implement backtracking

    def solve(self) -> None:
        """
        @brief Attempts to solve the board by applying constraint propigation.
        """
        if self.propigate_constraints():
            return True
        else:
            return False
