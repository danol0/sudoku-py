import numpy as np
from src.sudoku.board import SudokuBoard
import pytest

# test cases adapted from http://sudopedia.enjoysudoku.com/Invalid_Test_Cases.html

# puzzles with less that 17 clues should raise a warning but be solved
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

# puzzles with no solution should raise a value error
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
invalid_puzzles = [
    box_duplicate,
    column_duplicate,
    row_duplicate,
    invalid_square,
    invalid_box,
    invalid_row,
]

# valid puzzles should be solved without raising any errors
solved = (
    "974236158638591742125487936316754289742918563589362417867125394253649871491873625"
)
last_square = (
    "2564891733746159829817234565932748617128.6549468591327635147298127958634849362715"
)
naked_singles = (
    "3.542.81.4879.15.6.29.5637485.793.416132.8957.74.6528.2413.9.655.867.192.965124.8"
)
hidden_singles = (
    "..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4.."
)
valid_puzzles = [solved, last_square, naked_singles, hidden_singles]


def load_from_string(input_string: str) -> np.ndarray:
    """
    Modified input loader for test cases.
    """
    # Extract all digits and dots from the file & replace dots with zeros
    numbers = [
        int(char) if char.isdigit() else 0
        for char in input_string
        if char.isdigit() or char == "."
    ]
    return np.array(numbers).reshape((9, 9))


# test that puzzles with insufficient clues raise a warning but are solved
def test_warning_puzzles():
    for puzzle in warning_puzzles:
        with pytest.warns(UserWarning):
            initial_state = load_from_string(puzzle)
            board = SudokuBoard(initial_state)
        assert board.solve(), f"Test failed for puzzle: {puzzle}"


# test that puzzles with no solution raise a value error
def test_invalid_puzzles():
    for puzzle in invalid_puzzles:
        with pytest.raises(ValueError):
            initial_state = load_from_string(puzzle)
            board = SudokuBoard(initial_state)
            assert board.solve(), f"Test failed for puzzle: {puzzle}"


# test that valid puzzles are solved
def test_valid_puzzles():
    for puzzle in valid_puzzles:
        initial_state = load_from_string(puzzle)
        board = SudokuBoard(initial_state)
        assert board.solve(), f"Test failed for puzzle: {puzzle}"
