import pytest
import numpy as np
import src.sudoku.tools as st


@pytest.fixture
def initial_state(tmp_path):
    # simulate an input file
    state_data = "85...24..72......9..4....invalid.....1.7..23.5...9...4...characters........8..7..17..........36.4."
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


@pytest.fixture
def invalid_initial_state(tmp_path):
    # simulate an input file
    state_data = "85...24..72......9..4"
    file_path = tmp_path / "initial_state.txt"
    file_path.write_text(state_data)
    return str(file_path)


def test_load_initial_state_shape(initial_state):
    assert st.load_initial_state_file(initial_state).shape == (9, 9)


def test_load_initial_state_dtype(initial_state):
    assert st.load_initial_state_file(initial_state).dtype == np.int64


def test_load_initial_state_values(initial_state):
    initial_state_array = st.load_initial_state_file(initial_state)
    assert np.all(initial_state_array >= 0)
    assert np.all(initial_state_array <= 9)
    assert initial_state_array[0][0] == 8
    assert initial_state_array[0][1] == 5
    assert initial_state_array[0][2] == 0
    assert initial_state_array[0][3] == 0
    assert initial_state_array[8][8] == 0


def test_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        st.load_initial_state_file("does_not_exist.txt")


def test_invalid_initial_state(invalid_initial_state):
    with pytest.raises(ValueError):
        st.load_initial_state_file(invalid_initial_state)
