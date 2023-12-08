from src.sudoku.tools import load_initial_state
import pytest
import numpy as np

# This file contains test cases for the load_initial_state() function.


# using pytest fixtures to simulate input files
@pytest.fixture
def valid_initial_state(tmp_path):
    """
    Simulate a valid input file.
    """
    state_data = "85...24..72......9..4....invalid.....1.7..23.5...9...4...chars........8..7..17..........36.4."
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


@pytest.fixture
def invalid_initial_state(tmp_path):
    """
    Simulate an input file with invalid characters.
    """
    state_data = "85...24..72......9..4"
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


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
        load_initial_state(complete_initial_state),
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


def test_load_initial_state_from_string():
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
            load_initial_state(input),
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


def test_load_initial_state_object(valid_initial_state):
    """
    Test case to check that the initial state has the correct properties.
    """
    assert load_initial_state(valid_initial_state).shape == (9, 9)
    assert load_initial_state(valid_initial_state).dtype == np.int64


def test_load_initial_state_values(valid_initial_state):
    """
    Test cases to check that the initial state has the correct values.
    """
    initial_state_array = load_initial_state(valid_initial_state)
    assert np.all(initial_state_array >= 0)
    assert np.all(initial_state_array <= 9)
    assert initial_state_array[0][0] == 8
    assert initial_state_array[0][1] == 5
    assert initial_state_array[0][2] == 0
    assert initial_state_array[0][3] == 0
    assert initial_state_array[8][8] == 0


def test_invalid_file_path():
    """
    Test case to check that a value error is raised when the input file is not found.
    """
    with pytest.raises(ValueError):
        load_initial_state("does_not_exist.txt")


def test_invalid_initial_state(invalid_initial_state):
    """
    Test case to check that a value error is raised when the input file contains invalid characters.
    """
    with pytest.raises(ValueError):
        load_initial_state(invalid_initial_state)


def test_invalid_input_type():
    """
    Test case to check that a value error is raised when the input is not a file path or a string.
    """
    with pytest.raises(TypeError):
        load_initial_state((1, 2, 3))
        load_initial_state(123)
        load_initial_state([1, 2, 3])
        load_initial_state(np.array([1, 2, 3]))
        load_initial_state(np.zeros((9, 9)))
        load_initial_state(None)
