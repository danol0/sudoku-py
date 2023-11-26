import numpy as np


def load_initial_state_file(input_file: str) -> np.ndarray:
    """
    Load the initial state of the puzzle from the specified input file, allowing for a range of input formats.

    Parameters:
        input_file (str): Path to file containing the initial state. Must contain exactly 81 digits & dots.

    Returns:
        numpy.ndarray: The initial state of the board as a 9x9 numpy array, with zeros representing empty cells.

    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If the input file does not contain exactly 81 digits & dots.
    """
    try:
        with open(input_file, "r") as file:
            # Extract all digits and dots from the file & replace dots with zeros
            numbers = [
                int(char) if char.isdigit() else 0
                for line in file
                for char in line
                if char.isdigit() or char == "."
            ]

        # Check that the extracted board is of the correct size
        if len(numbers) != 81:
            raise ValueError(
                "Please check the input file: must contain exactly 81 digits & full stops."
            )

        return np.array(numbers).reshape((9, 9))

    except FileNotFoundError as e:
        print(f"Error: File '{input_file}' not found.")
        raise e

    except ValueError as ve:
        print(str(ve))
        raise ve
