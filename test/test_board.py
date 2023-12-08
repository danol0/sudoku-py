from src.sudoku.board import sudokuBoard
import numpy as np
import pytest

# This file contains test cases for the sudokuBoard class.


def test_board_init_with_np_array():
    """
    Test case to check that the board is initialized correctly with a numpy array.
    """
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
    board = sudokuBoard(initial_state)
    assert np.array_equal(board.state, initial_state)


def test_board_init_with_list():
    """
    Test case to check that the board is initialized correctly with a list.
    """
    initial_state = [
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
    board = sudokuBoard(initial_state)
    assert np.array_equal(board.state, np.array(initial_state))


def test_no_initial_state():
    """
    Test case to check that a value error is raised when no initial state is provided.
    """
    with pytest.raises(TypeError):
        sudokuBoard()


def test_board_init_invalid_type():
    """
    Test cases to check that a type error is raised when the initial state is not a numpy array or list.
    """
    with pytest.raises(TypeError):
        sudokuBoard("invalid")
        sudokuBoard(1)
        sudokuBoard(1.0)
        sudokuBoard(True)
        sudokuBoard(None)
        sudokuBoard((1, 2, 3))


def test_board_init_invalid_shape():
    """
    Test cases to check that a value error is raised when the initial state is not of shape (9, 9).
    """
    initial_state_list = [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
    ]
    initial_state_array = np.zeros((10, 10))
    with pytest.raises(ValueError):
        sudokuBoard(initial_state_list)
        sudokuBoard(initial_state_array)


def test_board_init_invalid_dtype():
    """
    Test cases to check that a value error is raised when the initial state is not of dtype int.
    """
    initial_state_array = np.array(
        [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 5, 0, 4.5],
            [0, 0, 0, 0, 5, 0, 1, 6, 9],
            [0, 8, 0, 0, 0, 0, 3, 0, 5],
            [0, 7, 5, 0, 0, 0, 2, 9, 0],
            [4, 0, 6, 0, 0, 0, 0, 8, 0],
            [7, 6, 2, 0, 8, 0, 0, 0, 0],
            [1, 0, 3, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 0],
        ]
    )
    initial_state_list = [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4.5],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]

    with pytest.raises(ValueError):
        sudokuBoard(initial_state_array)
        sudokuBoard(initial_state_list)


def test_board_init_invalid_values():
    """
    Test cases to check that a value error is raised when the initial state contains values outside of 0-9.
    """
    initial_state_array = np.array(
        [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 5, 0, 4],
            [0, 0, 0, 0, 5, 0, 1, 6, 9],
            [0, 8, 0, 0, 0, 0, 3, 0, 5],
            [0, 7, 5, 0, 0, 0, 2, 9, 0],
            [4, 0, 6, 0, 0, 0, 0, 8, 0],
            [7, 6, 2, 0, 8, 0, 0, 0, 0],
            [1, 0, 3, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 10],
        ]
    )
    initial_state_list = [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 10],
    ]
    with pytest.raises(ValueError):
        sudokuBoard(initial_state_array)
        sudokuBoard(initial_state_list)


def test_board_display():
    """
    Test case to check that the board is correctly represented as a string.
    """
    initial_state = np.ones(81, dtype=int).reshape(9, 9)
    board = sudokuBoard(initial_state)
    assert (
        str(board) == "111|111|111\n"
        "111|111|111\n"
        "111|111|111\n"
        "---+---+---\n"
        "111|111|111\n"
        "111|111|111\n"
        "111|111|111\n"
        "---+---+---\n"
        "111|111|111\n"
        "111|111|111\n"
        "111|111|111\n"
    )


def test_board_constraints():
    """
    Test case to check that the constraints are applied correctly.

    The initial state is solvable through constraints alone. The function checks that the
    possible values are correctly updated and that the board is solved.
    """
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
    board = sudokuBoard(initial_state)
    assert board.possible_values[3, 7] == {7}
    assert board.possible_values[8, 8] == {2}
    solved = board.propagate_constraints()  # should solve the board
    assert solved
    assert board.state[3, 7] == 7
    assert board.state[8, 8] == 2


def test_board_backtrack():
    """
    Test case to check that the board is solved through backtracking.

    The initial state is not solvable through constraints alone. The function checks that the
    solve method returns True, indicating that backtracking was required to solve the board.

    Further test cases for solve functionality can be found in test_board_solve.py.
    """
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
    board = sudokuBoard(initial_state)
    assert not board.propagate_constraints()  # not solvable through constraints alone
    assert board.solve()  # thus backtracking is required


def test_related_cells():
    """
    Test case to check that the related cells are correctly identified.
    """
    grid = np.array(
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    # should raise multiple solutions warning
    with pytest.warns(UserWarning):
        board = sudokuBoard(grid)
    index = (0, 4)
    related = board.related_cells(grid, index)
    assert related == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    index = (4, 0)
    related = board.related_cells(grid, index)
    assert related == {0, 1}
    index = (2, 4)
    related = board.related_cells(grid, index)
    assert related == {0, 4, 5, 6}
