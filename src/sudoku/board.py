import numpy as np
import warnings
import os


class sudokuBoard:
    """
    This class contains methods for initializing and checking the validity of a Sudoku board.

    Parameters
    ----------
    initial_state : str or numpy.ndarray[int] or list[list[int]]
        The initial state of the board. Can be provided as a string, a file path, or a 9x9 array.

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
        If the initial state is not a 9x9 array or contains invalid values.

    Returns
    -------
    self : object
        Initialized SudokuBoard object.

    See Also
    --------
    sudokuSolver :
        Child class of SudokuBoard that contains methods for solving.

    Examples
    --------
    Load the initial state from a file:

    >>> board = sudokuBoard("input.txt")
    Loading initial state from file: input.txt

    Load the initial state from a string:

    >>> board = sudokuBoard("594167832618239574237458169981726345375841296426395781762584913143972658859613472")
    Loading initial state from string.

    Initialize directly with an array:

    >>> initial_state = [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ]
    >>> board = sudokuBoard(initial_state)

    The board can be printed in a readable format:

    >>> print(board)
    483|921|657
    967|345|821
    251|876|493
    ---+---+---
    548|132|976
    729|564|138
    136|798|245
    ---+---+---
    372|689|514
    814|253|769
    695|417|382

    The board in its current state can be saved to a file:

    >>> board.save("solution.txt")

    Invalid boards will raise an error:

    >>> invalid_state = [
        [0, 0, 0, 0, 0, 0, 1, 2, 3],
        [0, 0, 9, 0, 0, 0, 0, 4, 5],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    >>> board = sudokuBoard(invalid_state)
    ValueError: The cell in row 2 and column 7 has no possible values. This puzzle has no solutions.

    Valid puzzles with multiple solutions will raise a warning:

    >>> board = sudokuBoard("........................................1........................................")
    WARNING: The puzzle has multiple solutions.
    """

    def __init__(self, initial_state: str | np.ndarray | list[list[int]]) -> None:
        """
        Initializes the board object from the specified initial state. Loads directly from array like objects,
        or uses the load_initial_state method to parse strings and file paths.
        """
        # use load_initial_state method to parse input if given as a string or file path
        if isinstance(initial_state, str):
            initial_state = self.load_initial_state(initial_state)

        # convert initial state to numpy array if necessary
        if isinstance(initial_state, list):
            try:
                initial_state = np.array(initial_state)
            except TypeError:
                raise TypeError("Error converting initial state to numpy array.")

        # the following checks ensure that the initial state is a 9x9 array of integers
        if not isinstance(initial_state, np.ndarray):
            raise TypeError("Initializing board with an object of incorrect type.")

        if initial_state.shape != (9, 9):
            try:
                initial_state = initial_state.reshape(9, 9)
            except ValueError:
                raise ValueError("Initializing board with an array of incorrect shape.")

        if initial_state.dtype != np.int64:
            raise ValueError("Initializing board with an array of incorrect dtype.")

        if np.logical_or(initial_state < 0, initial_state > 9).any():
            raise ValueError("Initializing board with array containing invalid values.")

        # puzzles with less than 17 clues have multiple solutions. source: https://arxiv.org/abs/2305.01697
        if np.count_nonzero(initial_state) < 17:
            warnings.warn("WARNING: The puzzle has multiple solutions.")

        # initialize indices and state attributes
        self.indices = [(i, j) for i in range(9) for j in range(9)]
        self.state = initial_state

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

    def load_initial_state(self, input: str) -> np.ndarray:
        """
        Load the initial state of a puzzle to a 9x9 array from a file or a string.

        Parameters
        ----------
        input : str
            Path to file containing the initial state or the initial state as a string.
            Must contain exactly 81 digits & dots (dots & zeros represent empty cells).

        Returns
        -------
        state : numpy.ndarray
            The initial state of the board as a 9x9 numpy array, with zeros representing empty cells.

        Raises
        ------
        FileNotFoundError :
            If the input file is not found.
        ValueError :
            If the input does not contain exactly 81 digits & dots.
        """

        # Check if the input is a file or a string
        if os.path.isfile(input):
            print(f"Loading initial state from file: {input}")
            with open(input, "r") as file:
                puzzle = file.read()
        else:
            print("Loading initial state from string.")
            puzzle = input

        # Extract all digits and dots from the input & replace dots with zeros
        board = [
            int(char) if char.isdigit() else 0
            for char in puzzle
            if char.isdigit() or char == "."
        ]

        # Check that the extracted board is of the correct size
        if len(board) != 81:
            raise ValueError(
                "Please check the input: must contain exactly 81 digits & full stops."
            )

        return np.array(board).reshape((9, 9))

    def update_possible_values(self) -> None:
        """
        Updates the possible values attribute given the current state of the board.

        Note
        ----
        The possible values attribute is updated in-place.

        Raises
        ------
        ValueError
            If a cell has no possible values, so the board is invalid.
        """
        # for empty cells, remove values in related cells from the possible values
        for index in self.indices:
            if self.state[index] == 0:
                self.possible_values[index] -= self.related_cells(self.state, index)

                # if no possible values, the board is invalid
                if self.possible_values[index] == set():
                    raise ValueError(
                        f"The cell in row {index[0]+1} and column {index[1]+1} has no possible values. "
                        "This puzzle has no solutions."
                    )

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

    def save(self, filename: str) -> None:
        """
        Saves the current state of the board to a file.

        Parameters
        ----------
        filename : str
            The name of the file to save to.
        """
        with open(filename, "w") as file:
            file.write(str(self))
