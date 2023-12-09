import numpy as np
import os


def load_initial_state(input: str) -> np.ndarray:
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

    Examples
    --------
    Load the initial state from a file:

    >>> load_initial_state("input.txt")
    Loading initial state from file: input.txt
    array([[5, 9, 4, 0, 0, 0, 1, 6, 7],
           [6, 0, 0, 2, 3, 9, 0, 5, 0],
           [0, 0, 0, 4, 5, 8, 0, 0, 0],
           [9, 8, 1, 7, 2, 6, 3, 4, 5],
           [3, 7, 5, 8, 4, 1, 2, 9, 6],
           [4, 2, 6, 3, 9, 5, 7, 8, 1],
           [7, 6, 2, 5, 8, 4, 9, 1, 3],
           [1, 4, 3, 9, 7, 2, 6, 5, 8],
           [8, 5, 9, 6, 1, 3, 4, 7, 2]])


    Load the initial state from a string:

    >>> load_initial_state("594167832618239574237458169981726345375841296426395781762584913143972658859613472")
    Loading initial state from string.
    array([[5, 9, 4, 1, 6, 7, 8, 3, 2],
           [6, 1, 8, 2, 3, 9, 5, 7, 4],
           [2, 3, 7, 4, 5, 8, 1, 6, 9],
           [9, 8, 1, 7, 2, 6, 3, 4, 5],
           [3, 7, 5, 8, 4, 1, 2, 9, 6],
           [4, 2, 6, 3, 9, 5, 7, 8, 1],
           [7, 6, 2, 5, 8, 4, 9, 1, 3],
           [1, 4, 3, 9, 7, 2, 6, 5, 8],
           [8, 5, 9, 6, 1, 3, 4, 7, 2]])
    """
    # Check if the input is a file or a string
    if isinstance(input, str):
        if os.path.isfile(input):
            print(f"Loading initial state from file: {input}")
            with open(input, "r") as file:
                puzzle = file.read()
        else:
            print("Loading initial state from string.")
            puzzle = input
    else:
        raise TypeError("Invalid input type. Please provide a file path or a string.")

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
