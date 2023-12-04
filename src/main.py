from sudoku.tools import load_initial_state
from sudoku.board import sudokuBoard
import sys


# check that a puzzle was passed
initial_state = sys.argv[1] if len(sys.argv) > 1 else None
if initial_state is None:
    raise ValueError("Please specify a puzzle.")

# load the initial state
state = load_initial_state(initial_state)

# initialize board
board = sudokuBoard(state)

# solve board
board.solve()

print(board)

# save the solution
board.save("solution.txt")
