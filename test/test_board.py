from src.sudoku.board import sudokuBoard
import numpy as np
import pytest

# This file contains test cases for the sudokuBoard class


# ---------------------------------- Validation -----------------------------------


def test_contradiction():
    """
    Test case to check that initializing boards with a contradiction raises an error.
    """
    contradiction_complete = "594167832618239574237458169981726345375841296426395781762584913143972658859613472"
    box_duplicate = "..9.7...5..21..9..1...28....7...5..1..851.....5....3.......3..68........21.....87"
    column_duplicate = "6.159.....9..1............4.7.314..6.24.....5..3....1...6.....3...9.2.4......16.."
    row_duplicate = ".4.1..35.............2.5......4.89..26.....12.5.3....7..4...16.6....7....1..8..2."
    warning_puzzles = [
        contradiction_complete,
        box_duplicate,
        column_duplicate,
        row_duplicate,
    ]
    for puzzle in warning_puzzles:
        with pytest.raises(ValueError):
            sudokuBoard(puzzle)


def test_insufficient_clues():
    """
    Test function to verify that a warning is raised for puzzles with insufficient clues
    """
    empty_board = "................................................................................."
    single_clues = "........................................1........................................"
    insufficient_clues = "...........5....9...4....1.2....3.5....7.....438...2......9.....1.4...6.........."
    warning_puzzles = [empty_board, single_clues, insufficient_clues]
    for puzzle in warning_puzzles:
        with pytest.warns(UserWarning):
            sudokuBoard(puzzle)


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
        "002|030|008\n"
        "000|008|000\n"
        "031|020|000\n"
        "---+---+---\n"
        "060|050|270\n"
        "010|000|050\n"
        "204|060|031\n"
        "---+---+---\n"
        "000|080|605\n"
        "000|000|013\n"
        "005|310|400",
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


# Using pytest fixtures to test loading from file
@pytest.fixture
def complete_initial_state(tmp_path):
    """
    Simulate an input file of a complete board.
    """
    state_data = "365427819487931526129856374852793641613248957974165283241389765538674192796512438"
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
                [3, 6, 5, 4, 2, 7, 8, 1, 9],
                [4, 8, 7, 9, 3, 1, 5, 2, 6],
                [1, 2, 9, 8, 5, 6, 3, 7, 4],
                [8, 5, 2, 7, 9, 3, 6, 4, 1],
                [6, 1, 3, 2, 4, 8, 9, 5, 7],
                [9, 7, 4, 1, 6, 5, 2, 8, 3],
                [2, 4, 1, 3, 8, 9, 7, 6, 5],
                [5, 3, 8, 6, 7, 4, 1, 9, 2],
                [7, 9, 6, 5, 1, 2, 4, 3, 8],
            ]
        ),
    )


def test_board_init_invalid_type():
    """
    Test cases to check that a type error is raised when the initial state is invalid.
    """
    for initial_state in [
        1,
        1.0,
        True,
        (1, 2, 3),
        None,
        [1, 2, 3],
        np.array([1, 2, 3]),
    ]:
        with pytest.raises(ValueError):
            sudokuBoard(initial_state)


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
    for initial_state in ["invalid", "123445689", "does_not_exist.txt"]:
        with pytest.raises(ValueError):
            sudokuBoard(initial_state)


def test_board_init_invalid_values():
    """
    Test cases to check that a value error is raised when the initial state contains values outside of 0-9.
    """
    initial_state_array = np.array(
        [
            [-1, 0, 0, 0, 0, 7, 0, 0, 0],
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
        [-1, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 10],
    ]
    for initial_state in [initial_state_array, initial_state_list]:
        with pytest.raises(ValueError):
            sudokuBoard(initial_state)


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
    assert board.related_cells((0, 4)) == {1, 2, 3, 4, 5, 6, 7, 8, 9}
    assert board.related_cells((0, 4), exclude_index=True) == {1, 2, 3, 4, 6, 7, 8, 9}
    assert board.related_cells((4, 4)) == {5}
    assert board.related_cells((4, 0)) == {1}
    assert board.related_cells((2, 4)) == {4, 5, 6}


def test_board_validate_no_contradictions():
    """
    Test case to check that the validate method returns True when there are no contradictions in the board.
    """
    solved = "974236158638591742125487936316754289742918563589362417867125394253649871491873625"
    valid = "974236158630591700000480936316754289742918563589302417867125394250649871491873625"
    board = sudokuBoard(solved)
    assert board.validate()
    board = sudokuBoard(valid)
    assert board.validate()
