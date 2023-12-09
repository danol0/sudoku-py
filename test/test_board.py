from src.sudoku.board import sudokuBoard
import numpy as np
import pytest

# This file contains test cases for the sudokuBoard class


# ------------------------------- Initialization ---------------------------------


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


def test_board_init_with_string():
    """ "
    Test case to check that the initial state is loaded correctly from a string.
    """

    input_formats = [
        "..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4..",
        "002030008000008000031020000060050270010000050204060031000080605000000013005310400",
        "002|030|008\n000|008|000\n031|020|000\n---+---+---\n060|050|270\n010|000|050\n204|060|031\n---+---+---\n000|080|605\n000|000|013\n005|310|400",
    ]

    for input in input_formats:
        assert np.array_equal(
            sudokuBoard(input).state,
            np.array(
                [
                    [0, 0, 2, 0, 3, 0, 0, 0, 8],
                    [0, 0, 0, 0, 0, 8, 0, 0, 0],
                    [0, 3, 1, 0, 2, 0, 0, 0, 0],
                    [0, 6, 0, 0, 5, 0, 2, 7, 0],
                    [0, 1, 0, 0, 0, 0, 0, 5, 0],
                    [2, 0, 4, 0, 6, 0, 0, 3, 1],
                    [0, 0, 0, 0, 8, 0, 6, 0, 5],
                    [0, 0, 0, 0, 0, 0, 0, 1, 3],
                    [0, 0, 5, 3, 1, 0, 4, 0, 0],
                ]
            ),
        )


@pytest.fixture
def complete_initial_state(tmp_path):
    """
    Simulate an input file of a complete board.
    """
    state_data = "594167832618239574237458169981726345375841296426395781762584913143972658859613472"
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


def test_load_initial_state_from_file(complete_initial_state):
    """
    Test case to check that the initial state is loaded correctly from a file.
    """
    assert np.array_equal(
        sudokuBoard(complete_initial_state).state,
        np.array(
            [
                [5, 9, 4, 1, 6, 7, 8, 3, 2],
                [6, 1, 8, 2, 3, 9, 5, 7, 4],
                [2, 3, 7, 4, 5, 8, 1, 6, 9],
                [9, 8, 1, 7, 2, 6, 3, 4, 5],
                [3, 7, 5, 8, 4, 1, 2, 9, 6],
                [4, 2, 6, 3, 9, 5, 7, 8, 1],
                [7, 6, 2, 5, 8, 4, 9, 1, 3],
                [1, 4, 3, 9, 7, 2, 6, 5, 8],
                [8, 5, 9, 6, 1, 3, 4, 7, 2],
            ]
        ),
    )


def test_board_init_invalid_type():
    """
    Test cases to check that a type error is raised when the initial state is invalid.
    """
    with pytest.raises(TypeError):
        sudokuBoard(1)
        sudokuBoard(1.0)
        sudokuBoard(True)
        sudokuBoard((1, 2, 3))
        sudokuBoard()
        sudokuBoard([1, 2, 3])
        sudokuBoard(np.array([1, 2, 3]))
        sudokuBoard(np.zeros((9, 9), dtype=float))
        sudokuBoard(None)


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


def test_board_init_invalid_string():
    """
    Test cases to check that a value error is raised when the initial state is not a valid string.
    """
    with pytest.raises(ValueError):
        sudokuBoard("invalid")
        sudokuBoard("123445689")
        sudokuBoard("does_not_exist.txt")


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


# ------------------------------- Display ---------------------------------


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


# ------------------------------- Constraints ---------------------------------


def test_board_possible_values():
    """
    Test case to check that the possible values are updated correctly.
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
