# sudoku-py: Solving Sudoku with Python

## About
This project is a lightweight python program for solving Sudoku puzzles. It using a combination of constraint propagation and brute-force search to find solutions, and can be run from the command line or imported as a package.

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Docker](#docker)
- [Documentation](#documentation)
- [Change log](#change-log)
- [Credits](#credits)

## Installation
The program requires only numpy to run, with pytest used for testing and sphinx for documentation. These dependencies are included in `requirements.txt` and can be installed by running:
```bash
pip install -r requirements.txt
```
from the root directory. To run the unit tests, run:
```bash
pytest
```

## Usage
### Command line
The program can be run from the command line with:
```bash
python src/main.py
```
The puzzle specified by the `input_state` key in the `config.json` file will be loaded and solved, with the solution printed to the terminal.

Note that the `initial_state` key can be either a file path to a text file containing the puzzle, or a string representation of the puzzle itself. The program will attempt to load from a file first and revert to a string if this fails, notifying the user if this is the case.

A puzzle can also be passed as a command line argument, in which case the `input_state` in the config file will be ignored. As before, this argument can be either a file path:
```bash
python src/main.py input.txt
```
or a string representation of the puzzle:
```bash
python src/main.py 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
```

Custom arguments for the solver can also be specified in the `config.json` file. The following options are available:
- `strategy`: the strategy to use for solving the puzzle. Options are `auto` (which attempts constraint propagation
        and then backtracking), `constraint_propagation` or `backtracking`. Default is `auto`.
- `max_solve_time`: the maximum time (in seconds) to spend solving the puzzle. Default is 60.
- `save_path`: filepath to save the solution to. Default is `false`, which does not save the solution.

### Valid Inputs
The input puzzle must contain exactly 81 digits or full stops, with 0s and full stops representing empty cells. All other characters will be ignored by the file loader. For example, the following are all valid inputs:
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
### Importing as a package
It is also possible to use this project as a python package. The sudoku package contains two modules:
- `board`: contains the sudokuBoard class, which contains methods for initializing and checking the validity of a board.
- `solver`: contains the sudokuSolver child class, which contains methods for solving Sudoku puzzles.

Example usage:

```python
import sudoku

board = sudoku.solver.sudokuSolver(state)
board.solve()
```
The solved board can then be printed to the terminal and/or saved to a file:
```python
board.save("output.txt")
print(board)
```
For more information on the classes and methods available, please see the [documentation](#documentation).

## Features

### Solving strategies:
#### Constraint propagation

Applies a reasoning algorithm to reduce the search space by assigning and removing values from cells:
- If a cell has only one possible value, it must be that value
- This value can then be removed from the possible values of all related cells

These steps are propagated until no further changes can be made.

#### Backtracking search

If constraint propagation is unable to solve the puzzle, a backtracking search is applied to the reduced search space.
Backtracking is a depth-first search, where board states are explored recursively:
- Allowed values are assigned to empty cells in turn (in order of increasing number of allowed values)
- If a valid solution is found, the search is complete
- If no more allowed values can be assigned, the search backtracks to the previous state and tries a different value

Backtracking is guaranteed to find a solution if there is one, given sufficient time.

### Other Features
- Wide range of allowed puzzle formats
- Detailed puzzle validation that provides relevant feedback for invalid puzzles
- Customizable solver options
- Ability to save solutions to file
- Robust and helpful error messages

## Docker
This project can be run in a Docker container. To build the container, from the root directory of the project run:
```bash
docker build -t sudoku-py .
```
The container can then be run with:
```bash
docker run -d -t --name=sudoku sudoku-py
```
Start a bash session in the container with:
```bash
docker exec -it sudoku bash
```
Once in the container, running `pytest` will check if the installation is working correctly.
From here the program can be run as described above in [Command line](#command-line) - either passing the input as a string or by first copying an input file into the container with `docker cp`.


## Documentation
This project uses Sphinx for documentation, which is included in the requirements.txt.
To build the documentation, from the root directory of the project run:
```bash
sphinx-build -M html docs/source docs/build/
```
The documentation can then be viewed by opening `docs/build/index.html` in a web browser.

## Change log
- v1.2:
  - Solve functionality is now contained in a child class of sudokuBoard
  - Updated main.py to use config file
  - Custom solver options can now be specified in config file or on object initialization

- v1.1:
  - Improved backtracking search logic
  - Added ability to pass input as a string
  - Updated dockerfile to not run & exit on launch

- v1.0:
  - Initial release
  - Added constraint propagation and backtracking search

## Credits
This project was written by Daniel Owen-Lloyd, using [widely known techniques](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms) for solving Sudoku puzzles.
