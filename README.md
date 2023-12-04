# sudoku-py: A python package for solving Sudoku puzzles

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Docker](#docker)
- [Documentation](#documentation)
- [Change log](#change-log)
- [Credits](#credits)

## About
This project is a lightweight package for solving Sudoku puzzles. It using a combination of constraint propagation and brute-force to find solutions, and can be run from the command line or as a python module.

## Installation
The program requires only numpy to run, with pytest used for testing as sphinx for documentation. These dependencies can be installed by running:
```bash
pip install -r requirements.txt
```
To run the unit tests, run:
```bash
pytest
```

## Usage
### Command line
The program can be run from the command line with:
```bash
python src/main.py input.txt
```
where `input.txt` is a text file containing the puzzle to be solved. The input puzzle must contain exactly 81 digits or full stops, with 0s and full stops representing empty cells. All other characters will be ignored by the file loader. For example, the following are all valid inputs:
```
000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000
```
```
003020600900305001001806400008102900700000008006708200002609500800203009005010300
```
```
..2.3...8.....8....31.2..../.6..5.27..1.....5.2.4.6..31./...8.6.5.......13..531.4..
```
The input can also be passed directly as a string:
```bash
python src/main.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300
```

The program will print the solved puzzle to the terminal, or a raise an error if there is no valid solution.

### Module
It is also possible to use this project as a python package:
```python
import sudoku
state = sudoku.tools.load_initial_state("input.txt")
board = sudoku.board.sudokuBoard(state)
board.solve()
```
The solved board can then be printed to the terminal and/or saved to a file:
```python
print(board)
board.save("output.txt")
```
For more information on the classes and functions available, see the [documentation](#documentation).

## Features
### Constraint propagation

Applies logic to reduce the search space by assigning and removing values from cells.
- If a cell has only one possible value, it must be that value
- This value can then be removed from the possible values of all related cells

These steps are propagated until no further changes can be made.

### Backtracking search

If constraint propagation is unable to solve the puzzle, a backtracking search is applied to the reduced search space. Backtracking is a depth-first search, where board states are explored recursively.
- Allowed values are assigned to empty cells in turn
- If a valid solution is found, the search is complete
- If no more allowed values can be assigned, the search backtracks to the previous state and tries a different value

Backtracking is guaranteed to find a solution if there is one, given sufficient time.


## Docker
This project can be run in a Docker container. To build the container, from the root directory of the project run:
```bash
docker build -t sudoku-py .
```
To run the container, run:
```bash
docker run -d -t --name=sudoku sudoku-py
```
Start a bash session in the container with:
```bash
docker exec -it sudoku bash
```
From here the program can be run as described above in [Command line](#command-line).

By default, the `input.txt` file in the directory will be copied to the container. To use a different puzzle, either change the contents of input.txt or change the INPUT_FILE environment variable in the Dockerfile to point to a text file of your choice:
```dockerfile
ENV INPUT_FILE=your_file_here.txt
```

## Documentation
This project uses Sphinx for documentation. To build the documentation, first install Sphinx:
```bash
pip install sphinx
```
Then, from the root directory of the project, run:
```bash
sphinx-build -M html docs/source docs/build/
```
The documentation can then be viewed by opening `docs/build/index.html` in a web browser.

## Change log
- v1.0.1:
  - Improved backtracking search logic
  - Added ability to pass input as a string
  - Updated dockerfile to not run & exit on launch
- v1.0.0:
  - Initial release

## Credits
This project was written by Daniel Owen-Lloyd, using [widely known techniques](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms) for solving Sudoku puzzles.
