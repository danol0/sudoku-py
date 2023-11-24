import numpy as np

# TODO: Loading the entire file at once is best practice


def load_initial_state(input_file: str) -> np.ndarray:
    """
    @brief Load the initial state of the puzzle from the specified input file.

    The function attempts to be robust to a range of input formats. It looks only for numbers and full stops
    (which are treated as zeros/empty cells) in the input file, discarding all other characters. It then
    checks that the extracted board is of the correct size (9x9) and raises an error if not. This allows
    a range of typical board formats to be used.

    @param input_file: Path to file containing the initial state. Must contain exactly 81 digits & dots.
    @type input_file: str

    @return: The initial state of the puzzle as a 9x9 numpy array, with zeros representing empty cells.
    @rtype: numpy.ndarray
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
                "There are too many or too few digits in the input file: must be exactly 81."
            )

        return np.array(numbers).reshape((9, 9))

    except FileNotFoundError as e:
        print(f"Error: File '{input_file}' not found.")
        raise e

    except ValueError as ve:
        print(str(ve))
        raise ve
