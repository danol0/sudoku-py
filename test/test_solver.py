from src.sudoku.solver import sudokuSolver
import numpy as np
import pytest

# This file contains test cases for the sudokuSolver class.

# Test cases adapted from http://sudopedia.enjoysudoku.com/Test_Cases.html


# -------------------------- Puzzles with insufficient clues ---------------------------
# Expected behavior: raises a warning but still solves the puzzle

empty_board = (
    "................................................................................."
)
single_clues = (
    "........................................1........................................"
)
insufficient_clues = (
    "...........5....9...4....1.2....3.5....7.....438...2......9.....1.4...6.........."
)
warning_puzzles = [empty_board, single_clues, insufficient_clues]


# ------------------------------ Puzzles with no solution ------------------------------
# Expected behavior: raises a value error when attempting to solve

box_duplicate = (
    "..9.7...5..21..9..1...28....7...5..1..851.....5....3.......3..68........21.....87"
)
column_duplicate = (
    "6.159.....9..1............4.7.314..6.24.....5..3....1...6.....3...9.2.4......16.."
)
row_duplicate = (
    ".4.1..35.............2.5......4.89..26.....12.5.3....7..4...16.6....7....1..8..2."
)
invalid_square = (
    "..9.287..8.6..4..5..3.....46.........2.71345.........23.....5..9..4..8.7..125.3.."
)
invalid_box = (
    ".9.3....1....8..46......8..4.5.6..3...32756...6..1.9.4..1......58..2....2....7.6."
)
invalid_row = (
    "9..1....4.14.3.8....3....9....7.8..18....3..........3..21....7...9.4.5..5...16..3"
)
invalid_column = (
    "....41....6.....2...2......32.6.........5..417.......2......23..48......5.1..2..."
)
invalid_puzzles = [
    box_duplicate,
    column_duplicate,
    row_duplicate,
    invalid_square,
    invalid_box,
    invalid_row,
    invalid_column,
]


# ----------------------------------- Valid Puzzles -----------------------------------
# Expected behavior: puzzle solved

solved = (
    "974236158638591742125487936316754289742918563589362417867125394253649871491873625"
)
solved_solution = (
    "974236158638591742125487936316754289742918563589362417867125394253649871491873625"
)
last_square = (
    "2564891733746159829817234565932748617128.6549468591327635147298127958634849362715"
)
last_square_solution = (
    "256489173374615982981723456593274861712836549468591327635147298127958634849362715"
)
naked_singles = (
    "3.542.81.4879.15.6.29.5637485.793.416132.8957.74.6528.2413.9.655.867.192.965124.8"
)
naked_singles_solution = (
    "365427819487931526129856374852793641613248957974165283241389765538674192796512438"
)
hidden_singles = (
    "..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4.."
)
hidden_singles_solution = (
    "672435198549178362831629547368951274917243856254867931193784625486592713725316489"
)
valid_puzzles = [solved, last_square, naked_singles, hidden_singles]
valid_puzzles_solutions = [
    solved_solution,
    last_square_solution,
    naked_singles_solution,
    hidden_singles_solution,
]


def test_warning_puzzles():
    """
    Test function to verify correct behavior for puzzles with insufficient clues.

    For each puzzle in the warning_puzzles list, the function checks that a warning is raised
    but the puzzle is still solved.
    """
    for puzzle in warning_puzzles:
        with pytest.warns(UserWarning):
            board = sudokuSolver(puzzle)
        assert board.solve(), f"Test failed for puzzle: {puzzle}"


def test_invalid_puzzles():
    """
    Test function to verify correct behavior for puzzles with no solution.

    For each puzzle in the invalid_puzzles list, the function checks that a value error is raised
    when attempting to solve the puzzle.
    """
    for puzzle in invalid_puzzles:
        with pytest.raises(ValueError):
            board = sudokuSolver(puzzle)
            assert board.solve(), f"Test failed for puzzle: {puzzle}"


def test_valid_puzzles():
    """
    Test function to verify correct behavior for valid puzzles.

    For each puzzle in the valid_puzzles list, the function checks that the puzzle is solved
    and that the solution is correct.
    """
    for puzzle, solution in zip(valid_puzzles, valid_puzzles_solutions):
        board = sudokuSolver(puzzle)
        assert board.solve(), f"Test failed for puzzle: {puzzle}"
        assert np.array_equal(
            board.state, sudokuSolver(solution).state
        ), f"Test failed for puzzle: {puzzle}"


def test_board_backtrack():
    """
    Test case to check that the board is solved through backtracking.

    The initial state is not solvable through constraints alone. The function checks that the
    solve method returns True, indicating that backtracking was required to solve the board.
    """
    board = sudokuSolver(hidden_singles, strategy="constraint_propagation")
    assert not board.solve()
    board = sudokuSolver(hidden_singles, strategy="backtracking")
    assert board.solve()
    board = sudokuSolver(hidden_singles, strategy="auto")
    assert board.solve()


def test_board_constraint_propagation():
    """
    Test case to check that the board is solved through constraint propagation.

    The initial state is solvable through constraints alone.
    """
    constraints = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    board = sudokuSolver(constraints, strategy="constraint_propagation")
    assert board.solve()


def test_board_timeout():
    """
    Test case to check that the board times out.

    The initial state is not solvable within the time limit.
    """
    board = sudokuSolver(hidden_singles, max_solve_time=0.000001)
    assert not board.solve()
    board = sudokuSolver(hidden_singles, max_solve_time=60)
    assert board.solve()


# ------------------------------ Test cases for __init__ ------------------------------


def test_solver_init_valid_strategy():
    """
    Test case to verify that the solver initializes with a valid strategy.
    """
    initial_state = hidden_singles
    strategy = "auto"
    max_solve_time = 60
    solver = sudokuSolver(initial_state, strategy, max_solve_time)
    assert solver.strategy == strategy


def test_solver_init_invalid_strategy():
    """
    Test case to verify that the solver raises a ValueError for an invalid strategy.
    """
    initial_state = hidden_singles
    strategy = "invalid_strategy"
    max_solve_time = 60
    with pytest.raises(ValueError):
        sudokuSolver(initial_state, strategy, max_solve_time)


def test_solver_init_valid_max_solve_time():
    """
    Test case to verify that the solver initializes with a valid max_solve_time.
    """
    initial_state = hidden_singles
    strategy = "auto"
    max_solve_time = 60
    solver = sudokuSolver(initial_state, strategy, max_solve_time)
    assert solver.max_solve_time == max_solve_time


def test_solver_init_invalid_max_solve_time():
    """
    Test case to verify that the solver raises a ValueError for an invalid max_solve_time.
    """
    initial_state = hidden_singles
    strategy = "auto"
    max_solve_time = -1
    with pytest.raises(ValueError):
        sudokuSolver(initial_state, strategy, max_solve_time)
