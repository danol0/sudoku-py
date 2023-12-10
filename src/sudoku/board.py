import numpy as np
import warnings
import os


class sudokuBoard:
    """
    General class for representing a Sudoku board with methods for initializing, printing and saving.

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

    >>> board = sudokuBoard("365427819487931526129856374852793641613248957974165283241389765538674192796512438")
    Loading initial state from string.

    Initialize directly with an array:

    >>> initial_state = [
        [3, 6, 5, 4, 2, 7, 8, 1, 9],
        [4, 8, 7, 9, 3, 1, 5, 2, 6],
        [1, 2, 9, 8, 5, 6, 3, 7, 4],
        [8, 5, 2, 7, 9, 3, 6, 4, 1],
        [6, 1, 3, 2, 4, 8, 9, 5, 7],
        [9, 7, 4, 1, 6, 5, 2, 8, 3],
        [2, 4, 1, 3, 8, 9, 7, 6, 5],
        [5, 3, 8, 6, 7, 4, 1, 9, 2],
        [7, 9, 6, 5, 1, 2, 4, 3, 8]
    ]
    >>> board = sudokuBoard(initial_state)

    The board can be printed in a readable format:

    >>> print(board)
    365|427|819
    487|931|526
    129|856|374
    ---+---+---
    852|793|641
    613|248|957
    974|165|283
    ---+---+---
    241|389|765
    538|674|192
    796|512|438

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
    ValueError: This puzzle is invalid as the cell in row 2 and column 7 has no possible values.

    Valid puzzles with multiple solutions will raise a warning:

    >>> board = sudokuBoard("........................................1........................................")
    WARNING: The puzzle has multiple solutions.

    Initializing a completed board with a contradiction will raise an error:

    >>> board = sudokuBoard("594167832618239574237458169981726345375841296426395781762584913143972658859613472")
    ValueError: This board is invalid as the cell in row 1 and column 9 is a contradiction.
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
        elif isinstance(initial_state, list):
            try:
                initial_state = np.array(initial_state)
            except TypeError:
                raise TypeError("Error converting initial state to numpy array.")

        # the following checks ensure that the initial state is a 9x9 array of integers
        elif not isinstance(initial_state, np.ndarray):
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
        Readable string representation of the board.

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
            with open(input, "r") as file:
                puzzle = file.read()
        else:
            print("No file was found at specified input, treating as a puzzle string.")
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
                        f"This puzzle is invalid as the cell in row {index[0]+1} and column {index[1]+1} "
                        "has no possible values."
                    )

        # for a complete board, check for contradictions
        if np.all(self.state):
            for index in self.indices:
                if self.state[index] in self.related_cells(self.state, index):
                    raise ValueError(
                        f"This board is invalid as the cell in row {index[0]+1} and column {index[1]+1} "
                        "is a contradiction."
                    )

        return True

    def related_cells(self, grid: np.ndarray, index: tuple) -> set:
        """
        Returns the contents of all cells in the given grid that are related to the specified index.

        Note
        ----
        Related cells are those in the same row, column, or box as the given cell.

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

        # create a temporary copy of the grid
        masked_grid = np.copy(grid)

        # mask the cell at the given index in the temporary grid
        masked_grid[row, col] = 0

        related = {
            *masked_grid[row, :],
            *masked_grid[:, col],
            *masked_grid[box_row : box_row + 3, box_col : box_col + 3].flatten(),
        }

        return related

    def save(self, filepath: str) -> None:
        """
        Saves the current state of the board to a file.

        Parameters
        ----------
        filepath : str
            The filepath to save the board to.
        """
        with open(filepath, "w") as file:
            file.write(str(self))
