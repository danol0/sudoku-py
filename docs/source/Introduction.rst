sudoku-py: A python package for solving Sudoku puzzles
======================================================

About
-----

This project is a lightweight package for solving Sudoku puzzles. It
using a combination of constraint propagation and brute-force search to
find solutions, and can be run from the command line or as a python
module.

Contents
--------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Features <#features>`__
-  `Docker <#docker>`__
-  `Documentation <#documentation>`__
-  `Change log <#change-log>`__
-  `Credits <#credits>`__

Installation
------------

The program requires only numpy to run, with pytest used for testing as
sphinx for documentation. These dependencies can be installed by
running:

.. code:: bash

   pip install -r requirements.txt

To run the unit tests, run:

.. code:: bash

   pytest

Usage
-----

Command line
~~~~~~~~~~~~

The program can be run from the command line with:

.. code:: bash

   python src/main.py input.txt

where ``input.txt`` is a text file containing the puzzle to be solved.
The input puzzle must contain exactly 81 digits or full stops, with 0s
and full stops representing empty cells. All other characters will be
ignored by the file loader. For example, the following are all valid
inputs:

::

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

::

   003020600900305001001806400008102900700000008006708200002609500800203009005010300

::

   ..2.3...8.....8....31.2..../.6..5.27..1.....5.2.4.6..31./...8.6.5.......13..531.4..

The input can also be passed directly as a string:

.. code:: bash

   python src/main.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300

The program will print the solved puzzle to the terminal, or a raise an
error if there is no valid solution.

Module
~~~~~~

It is also possible to use this project as a python package:

.. code:: python

   import sudoku
   state = sudoku.tools.load_initial_state("input.txt")
   board = sudoku.board.sudokuBoard(state)
   board.solve()

The solved board can then be printed to the terminal and/or saved to a
file:

.. code:: python

   print(board)
   board.save("output.txt")

For more information on the classes and functions available, see the
`documentation <#documentation>`__.

Features
--------

Constraint propagation
~~~~~~~~~~~~~~~~~~~~~~

Applies logic to reduce the search space by assigning and removing
values from cells. - If a cell has only one possible value, it must be
that value - This value can then be removed from the possible values of
all related cells

These steps are propagated until no further changes can be made.

Backtracking search
~~~~~~~~~~~~~~~~~~~

If constraint propagation is unable to solve the puzzle, a backtracking
search is applied to the reduced search space. Backtracking is a
depth-first search, where board states are explored recursively. -
Allowed values are assigned to empty cells in turn - If a valid solution
is found, the search is complete - If no more allowed values can be
assigned, the search backtracks to the previous state and tries a
different value

Backtracking is guaranteed to find a solution if there is one, given
sufficient time.

Docker
------

This project can be run in a Docker container. To build the container,
from the root directory of the project run:

.. code:: bash

   docker build -t sudoku-py .

The container can then be run with:

.. code:: bash

   docker run -d -t --name=sudoku sudoku-py

Start a bash session in the container with:

.. code:: bash

   docker exec -it sudoku bash

Once in the container, running ``pytest`` will check if the installation
is working correctly. From here the program can be run as described
above in `Command line <#command-line>`__ - copying an input file into
the container can be done with ``docker cp``, or the input can be passed
directly as a string.

Documentation
-------------

This project uses Sphinx for documentation. To build the documentation,
first install Sphinx:

.. code:: bash

   pip install sphinx

Then, from the root directory of the project, run:

.. code:: bash

   sphinx-build -M html docs/source docs/build/

The documentation can then be viewed by opening
``docs/build/index.html`` in a web browser.

Change log
----------

-  v1.1:

   -  Improved backtracking search logic
   -  Added ability to pass input as a string
   -  Updated dockerfile to not run & exit on launch

-  v1.0:

   -  Initial release

Credits
-------

This project was written by Daniel Owen-Lloyd, using `widely known
techniques <https://en.wikipedia.org/wiki/Sudoku_solving_algorithms>`__
for solving Sudoku puzzles.
