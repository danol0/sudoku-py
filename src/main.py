import sys
import sudoku.tools as st
from sudoku.board import SudokuBoard

# default state file is input.txt
state_file = sys.argv[1] if len(sys.argv) > 1 else None
if state_file is None:
    raise ValueError("Please specify a state file.")

# load the initial state from file
state = st.load_initial_state_file(state_file)

# initialize board from state
board = SudokuBoard(state)

# solve board
board.solve()

print(board)
