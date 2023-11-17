import sys
import numpy as np

def load_initial_state(input_file):
    """
    Initialise the puzzle array from the input file.
    :param input_file: File containing the initial state, in the format specified by the instructions.
    :return: The initial state of the puzzle as a 9x9 numpy array.
    """

    with open(input_file, "r") as f:
        numbers = [int(char) for line in f for char in line if char.isdigit()]
    initial_state = np.array(numbers).reshape(9, 9)
    return initial_state


def output_state(state):
    """
    Output the state of the puzzle to stdout, in the format specified by the instructions.
    :param state: The state of the puzzle to output.
    :return: None
    """

    for row in range(9):
        if row == 3 or row == 6:
            print("---+---+---")
        for col in range(9):
            if col == 3 or col == 6:
                print("|", end="")
            print(state[row, col], end="")
        print("\n", end="")

output_state(load_initial_state(sys.argv[1]))
