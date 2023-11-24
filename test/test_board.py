import numpy as np
from src.sudoku.board import SudokuBoard
import pytest


def test_board_initialization():
    initial_state = np.ones(81, dtype=int).reshape(9, 9)
    board = SudokuBoard(initial_state)
    assert np.array_equal(board.state, initial_state)


def test_board_printing():
    initial_state = np.ones(81, dtype=int).reshape(9, 9)
    board = SudokuBoard(initial_state)
    assert (
        str(board)
        == "111|111|111\n111|111|111\n111|111|111\n---+---+---\n111|111|111\n111|111|111\n111|111|111\n---+---+---\n111|111|111\n111|111|111\n111|111|111\n"
    )


def test_board_invalid_initial_state():
    wrong_shape = np.ones(80, dtype=int).reshape(8, 10)
    wrong_type = np.linspace(1, 80, 81, dtype=float).reshape(9, 9)
    double_digit = np.linspace(10, 80, 81, dtype=int).reshape(9, 9)
    with pytest.raises(ValueError):
        SudokuBoard(wrong_shape)
    with pytest.raises(ValueError):
        SudokuBoard(wrong_type)
    with pytest.raises(ValueError):
        SudokuBoard(double_digit)


def test_board_constraint():
    initial_state = np.array(
        [
            [4, 8, 3, 9, 2, 1, 6, 5, 7],
            [9, 6, 7, 3, 0, 5, 8, 2, 1],
            [2, 5, 1, 0, 7, 6, 4, 9, 3],
            [5, 4, 8, 1, 3, 0, 9, 0, 6],
            [7, 2, 9, 5, 0, 4, 1, 3, 8],
            [0, 3, 6, 7, 9, 8, 2, 4, 5],
            [3, 7, 2, 0, 8, 9, 5, 1, 4],
            [8, 0, 4, 2, 5, 3, 7, 6, 9],
            [6, 9, 5, 4, 1, 7, 3, 8, 0],
        ]
    )
    board = SudokuBoard(initial_state)
    assert board.possible_values[3, 7] == {7}
    assert board.possible_values[8, 8] == {2}
    assert board.possible_values[0, 0] == {} or {4}  # TODO: depends on implimentation
    solved = board.propagate_constraints()  # should solve the board
    assert solved


def test_board_backtrack():
    initial_state = np.array(
        [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 5, 0, 4],
            [0, 0, 0, 0, 5, 0, 1, 6, 9],
            [0, 8, 0, 0, 0, 0, 3, 0, 5],
            [0, 7, 5, 0, 0, 0, 2, 9, 0],
            [4, 0, 6, 0, 0, 0, 0, 8, 0],
            [7, 6, 2, 0, 8, 0, 0, 0, 0],
            [1, 0, 3, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 0],
        ]
    )
    board = SudokuBoard(initial_state)
    constraints_solve = board.propagate_constraints()
    assert not constraints_solve
    solved = board.solve()
    assert solved
