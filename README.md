# Sudoku-Solver: A Sudoku solver written in Python

## About
This is a simple Sudoku solver written in Python. It uses simple constraint propigation to attempt to solve the board using reasoning, before falling back on a brute-force backtracking search. It is designed to be run from the command line with a single argument: the path to a text file containing the Sudoku puzzle to be solved.
```bash
python src/main.py input.txt
```

## Installation
This project is lightweight and requires only numpy to run, with pytest used for testing. These dependancies can be installed by running:
```bash
pip install -r requirements.txt
```

## Docker
This project can be run in a Docker container. To build the container, run:
```bash
docker build -t sudoku-solver .
```
To run the container, run:
```bash
docker run -it sudoku-solver
```
The container will run the solver on the example puzzle in `input.txt` and print the solution to the terminal. To use a different puzzle, either change the contents of input.txt or change the INPUT_FILE environment variable in the Dockerfile to point to a file of your choice:
```dockerfile
ENV INPUT_FILE=your_file_here.txt
```
## Features
### Simple constraint propagation:

Applies simple reasoning, following what is known as the "pencil mark" method:
- If a cell has only one possible value, it must be that value
- This value can then be removed from the possible values of all related cells

This process of checking and removing values is repeated until no more values can be removed.

### Brute-force backtracking search

If constraint propagation is unable to solve the grid, a recursive backtracking search is applied to the reduced search space.
- The algorithm recursively explores each possible value for a cell, backtracking if it reaches a dead end.
