import numpy as np


class SudokuBoard:
    """
    @brief Class representing the state of a sudoku board.
    """

    def __init__(self, initial_state: np.ndarray) -> None:
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
        self.state = initial_state

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
