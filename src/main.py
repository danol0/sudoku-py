import sys
import sudoku.tools as st
from sudoku.board import SudokuBoard
import time

board = SudokuBoard(st.load_initial_state_to_array(sys.argv[1]))
start = time.time()
board.solve()
end = time.time()
print("Time taken: ", end - start)
print(board)
