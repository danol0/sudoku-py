from .board import sudokuBoard
import numpy as np
import time


class sudokuSolver(sudokuBoard):
    """
    Child class of sudokuBoard that contains methods for solving puzzles.

    Parameters
    ----------
    initial_state : str or numpy.ndarray[int] or list[list[int]]
        The initial state of the board. Can be provided as a string, a file path, or a 9x9 array.

    strategy : str, optional
        The strategy to use for solving the puzzle. Options are 'auto' (which tries constraint propagation
        and then backtracking), 'constraint_propagation', and 'backtracking'.
        The default is 'auto'.

    max_solve_time : float, optional
        The maximum time in seconds to spend solving the puzzle. The default is 60.

    Attributes
    ----------
    start : float
        The time at which the solve method was called.

    Methods
    -------
    solve()
        Attempts to solve the board by calling constraint propagation and then backtracking.

    propagate_constraints()
        Assigns values for cells with only one possible value and propagates.

    backtrack(grid)
        Recursive, depth-first search on the given board state.

    See Also
    --------
    sudokuBoard :
        Parent class of sudokuSolver that contains methods for initializing boards.

    Examples
    --------
    Initialise and solve a board:

    >>> board = sudokuSolver("input.txt")
    Loading initial state from file: input.txt
    >>> board.solve()
    The puzzle was solved by constraint propagation in 0.002 seconds.
    >>> print(board)
    594|167|832
    618|239|574
    237|458|169
    ---+---+---
    981|726|345
    375|841|296
    426|395|781
    ---+---+---
    762|584|913
    143|972|658
    859|613|472

    A value error is raised if no solutions exist (Note: requires a strategy that includes backtracking):

    >>> board = sudokuSolver("invalid.txt")
    Loading initial state from file: invalid.txt
    >>> board.solve()
    ValueError: No solutions exist for this puzzle. Search took 0.012 seconds.
    """

    def __init__(
        self,
        initial_state: str | np.ndarray | list[list[int]],
        strategy: str = "auto",
        max_solve_time: int | float = 60,
    ) -> None:
        """
        Initializes the sudokuSolver object, making use of the input validation in the parent class.
        """

        super().__init__(initial_state)

        # check that the strategy is valid
        if strategy not in ["auto", "constraint_propagation", "backtracking"]:
            raise ValueError(
                "Invalid strategy. Options are 'auto', 'constraint_propagation', and 'backtracking'."
            )

        # check that the max_solve_time is valid
        if not isinstance(max_solve_time, (int, float)) or max_solve_time <= 0:
            raise ValueError("Invalid max_solve_time. Must be greater than zero.")

        self.strategy = strategy
        self.max_solve_time = max_solve_time
        self.start = None

    def propagate_constraints(self) -> bool:
        """
        Assigns values for cells with only one possible value and propagates.

        Note
        ----
        Assignment is to the state attribute.
        Propagation continues until no more updates are made or the board is full.

        Returns
        -------
        solved : bool
            True if the board is complete, False otherwise.
        """
        # if board is full, return
        if np.all(self.state):
            return True

        # if max time exceeded, return
        if time.time() - self.start >= self.max_solve_time:
            return False

        # update possible values for the current state
        self.update_possible_values()

        for index in self.indices:
            # if cell has only one possible value, assign it and propagate
            if len(self.possible_values[index]) == 1:
                self.state[index] = self.possible_values[index].pop()
                return self.propagate_constraints()

        # return False once propagation is complete
        return False

    def backtrack(self) -> bool:
        """
        Recursive, depth-first search on the board state.

        Returns
        -------
        solved : bool
            True if a solution was found, False otherwise.
        """
        # base case: if board is full, return
        if np.all(self.state):
            return True

        # if max time exceeded, return
        if time.time() - self.start >= self.max_solve_time:
            return False

        # this implements the MRV heuristic - see section 3.1.1 of report
        # find the index of the cell with the fewest possible values and search
        least_possible_values_index = np.argmax(
            [
                len(self.related_cells(self.state, index))
                if self.state[index] == 0
                else 0
                for index in self.indices
            ]
        )
        index = self.indices[least_possible_values_index]

        for value in self.possible_values[index] - self.related_cells(
            self.state, index
        ):
            # assign the value and recurse
            self.state[index] = value
            if self.backtrack():
                return True

            # if no solution found, reset the cell and try the next value
            self.state[index] = 0

        # return False if all values have been tried without finding a solution
        return False

    def solve(self) -> bool:
        """
        Attempts to solve the board by calling constraint propagation and then backtracking.

        Returns
        -------
        solved : bool
            True if the board was solved, False if no solutions exist.

        Raises
        ------
        ValueError
            If no solutions exist for the puzzle. The search time is included in the error message.
        """
        # check if the board is already solved
        if np.all(self.state):
            print("The board is already solved.")
            return True

        # start the timer
        self.start = time.time()

        # call each strategy if enabled
        if self.strategy != "backtracking" and self.propagate_constraints():
            print(
                f"The puzzle was solved by constraint propagation in {time.time() - self.start:.3} seconds."
            )
            return True
        elif self.strategy != "constraint_propagation" and self.backtrack():
            print(
                f"The puzzle was solved by backtracking in {time.time() - self.start:.3} seconds"
            )
            return True

        # If the puzzle is not solved, check why:
        # 1: Using only constraint propagation could not solve the puzzle
        elif time.time() - self.start < self.max_solve_time:
            if self.strategy == "constraint_propagation":
                print(
                    "The puzzle could not be solved by constraint propagation alone, consider backtracking."
                )
                return False
            # 2: No solutions exist for the puzzle
            else:
                raise ValueError(
                    f"No solutions exist for this puzzle. Search took {time.time() - self.start:.3} seconds."
                )
        # 3: The max solve time was exceeded
        else:
            print(
                f"Time limit of {self.max_solve_time:.1f} seconds reached, "
                "consider increasing the max solve time."
            )
            return False
