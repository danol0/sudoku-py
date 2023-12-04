from src.sudoku.tools import load_initial_state
import pytest
import numpy as np


# using pytest fixtures to simulate input files
@pytest.fixture
def valid_initial_state(tmp_path):
    # simulate an input file
    state_data = "85...24..72......9..4....invalid.....1.7..23.5...9...4...chars........8..7..17..........36.4."
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


@pytest.fixture
def invalid_initial_state(tmp_path):
    # simulate an input files
    state_data = "85...24..72......9..4"
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


def test_load_initial_state_from_file(tmp_path):
    state_data = "594167832618239574237458169981726345375841296426395781762584913143972658859613472"
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    assert np.array_equal(
        load_initial_state(str(file_path)),
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
    state_data = "594167832618239574237458169981726345375841296426395781762584913143972658859613472"
    assert np.array_equal(
        load_initial_state(state_data),
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


def test_load_initial_state_shape(valid_initial_state):
    assert load_initial_state(valid_initial_state).shape == (9, 9)


def test_load_initial_state_dtype(valid_initial_state):
    assert load_initial_state(valid_initial_state).dtype == np.int64


def test_load_initial_state_values(valid_initial_state):
    initial_state_array = load_initial_state(valid_initial_state)
    assert np.all(initial_state_array >= 0)
    assert np.all(initial_state_array <= 9)
    assert initial_state_array[0][0] == 8
    assert initial_state_array[0][1] == 5
    assert initial_state_array[0][2] == 0
    assert initial_state_array[0][3] == 0
    assert initial_state_array[8][8] == 0


def test_invalid_file_path():
    with pytest.raises(ValueError):
        load_initial_state("does_not_exist.txt")


def test_invalid_initial_state(invalid_initial_state):
    with pytest.raises(ValueError):
        load_initial_state(invalid_initial_state)
