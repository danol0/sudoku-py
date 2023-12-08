from . import board
from . import tools

"""
sudoku-py
=========

Python package for solving sudoku puzzles.

Modules
-------
- board: Defines the sudokuBoard class and its operations.
- tools: Provides utility functions for loading Sudoku puzzles.

Examples
--------
>>> import sudoku

# load the puzzle from file
>>> state = sudoku.tools.load_initial_state("input.txt")

# initialize board object
>>> board = sudoku.board.sudokuBoard(state)

# solve the puzzle
>>> board.solve()
The puzzle was solved by constraint propagation in 0.0045 seconds.

# display the solved puzzle
>>> print(board)
483|921|657
967|345|821
251|876|493
---+---+---
548|132|976
729|564|138
136|798|245
---+---+---
372|689|514
614|253|789
895|417|362
"""
