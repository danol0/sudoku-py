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
