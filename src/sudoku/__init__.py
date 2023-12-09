# import submodules for package
from . import board
from . import solver

"""
sudoku-py
=========

Python package for solving sudoku puzzles.

Modules
-------
- board: Defines the sudokuBoard class with methods for initializing a board state.
- solver: Defines the sudokuSolver class with methods for solving Sudoku puzzles.

Examples
--------
>>> import sudoku

# initialize board object
>>> board = sudoku.solver.sudokuSolver("input.txt")

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

# save the solved puzzle to a file
>>> board.save("solution.txt")
"""
