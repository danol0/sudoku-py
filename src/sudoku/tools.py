import numpy as np


def load_initial_state_to_array(input_file: str) -> np.ndarray:
    """
    @brief Load the initial state of the puzzle from the specified input file.

    @param input_file: Path to file containing the initial state. Must contain exactly 81 digits.
    @type input_file: str

    @return: The initial state of the puzzle as a 9x9 numpy array.
    @rtype: numpy.ndarray
    """

    try:
        with open(input_file, "r") as file:
            numbers = [int(char) for line in file for char in line if char.isdigit()]

        if len(numbers) != 81 or any(number < 0 or number > 9 for number in numbers):
            raise ValueError("The input file provided is not in the correct format.")

        return np.array(numbers).reshape(9, 9)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        raise

    except ValueError as ve:
        print(str(ve))
        raise

    except Exception as e:
        print(
            f"Error: An error occurred while loading the initial state file: {str(e)}"
        )
        raise
