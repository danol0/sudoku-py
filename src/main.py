import sys
import sudoku.tools as st
from sudoku.board import SudokuBoard

state = st.load_initial_state_to_array(sys.argv[1])
board = SudokuBoard(state)
print(board)
