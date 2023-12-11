from sudoku.solver import sudokuSolver
import sys
import json


def load_config():
    """
    Load the configuration from the config.json file.

    Returns
    -------
    config : dict
        The configuration settings.

    Raises
    -------
        FileNotFoundError :
            If the config.json file is not found.
    """
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Config file not found. Please create a config.json file in the root directory."
        )

    return config


def main():
    """
    Main entry point of the script.
    """
    # Load the configuration
    config = load_config()

    # Overwrite the config puzzle if user has specified one via the command line
    if len(sys.argv) == 2:
        initial_state = sys.argv[1]
        print("Loading puzzle from command line argument")
    elif len(sys.argv) > 2:
        raise ValueError(
            "Too many arguments provided. Accepts one argument, the path to the puzzle file, "
            "or none to load from the config file."
        )
    else:
        initial_state = config["initial_state"]
        print("Loading puzzle from config file")

    # Initialize the solver
    board = sudokuSolver(
        initial_state,
        strategy=config["strategy"],
        max_solve_time=config["max_solve_time"],
    )

    # Solve and print the board
    board.solve()
    print(board)

    # Save the board if a save path is specified
    if config["save_path"]:
        board.save(config["save_path"])


if __name__ == "__main__":
    main()
