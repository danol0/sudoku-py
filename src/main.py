from sudoku.solver import sudokuSolver
import sys

# check that a puzzle was passed as an argument
initial_state = sys.argv[1] if len(sys.argv) > 1 else None
if initial_state is None:
    raise ValueError("Please specify a puzzle.")

# initialize solver
board = sudokuSolver(initial_state)

# solve and print the board
board.solve()
print(board)
