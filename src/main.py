from sudoku.solver import sudokuSolver
import sys
import json
import warnings

# check that the config file exists
try:
    with open("config.json") as f:
        config = json.load(f)

except FileNotFoundError:
    warnings.warn("The config.json file does not exist, using default config.")
    config = {
        "initial_state": ".....7........95.4....5.169.8....3.5.75...29.4.6....8.762.8....1.39........6.....",
        "strategy": "auto",
        "max_solve_time": 60,
        "save_path": False,
    }

# overwrite the config puzzle if user has specified one via the command line
if len(sys.argv) == 2:
    initial_state = sys.argv[1]
    print("Loading puzzle from command line argument")
elif len(sys.argv) > 2:
    raise ValueError(
        "Too many arguments provided. Please provide a single filepath or puzzle string."
    )
else:
    initial_state = config["initial_state"]
    print("Loading puzzle from config file")

# initialize solver
board = sudokuSolver(
    initial_state, strategy=config["strategy"], max_solve_time=config["max_solve_time"]
)

# solve and print the board
board.solve()
print(board)

# save the board if a save path is specified
if config["save_path"]:
    board.save(config["save_path"])
