"""
~SudoCat~

Recursive Sudoku Solver
"""

import numpy as np
import time
import random
from load_data import load_data


# Solving the sudoku puzzle using a recursive method and returns the solved matrix
def solve_sudoku_rec(sudoku_mat , row , col):
    # End condition of the recursion, if the solution got to row 9 - the matrix is full
    if (row > 8):
        return sudoku_mat

    if sudoku_mat[row][col]:            # if a cell is already filled - skip it
        if (col < 8):                   # is it possible to shift to the next column?
            # call the function to check the next cell
            if solve_sudoku_rec(sudoku_mat , row , col+1)[0][0]:
                # if the next cell returned a value, this cell will return to the prior cell a value
                return sudoku_mat
        elif solve_sudoku_rec(sudoku_mat , row+1 , 0)[0][0]:      # shifts to the next row
            return sudoku_mat
        # if the next cell returned 0, this cell will return to the prior cell 0
        return [[0]]

    for digit in range(1,10):
        # run over the numbers possible for this empty cell
        if possible(sudoku_mat , row , col , digit):
            sudoku_mat[row][col] = digit	# if its possible to insert the number - put it in

            if (col < 8):	# shifts to the next cell
                if solve_sudoku_rec(sudoku_mat , row , col+1)[0][0]:
                    return sudoku_mat
            elif solve_sudoku_rec(sudoku_mat , row+1 , 0)[0][0]:
                return sudoku_mat
			# If the next cell returned 0, this cell will continue running on the possible numbers

	# If there is no number possible to insert into this cell, input 0 to terminate this cells value
    sudoku_mat[row][col] = 0
    return [[0]]	# return 0 to the prior cell to try another combination

# Checks whether it is possible to insert 'digit' in the given cell of
# sudoku_mat[row][col] or not
def possible(sudoku_mat , row , col , digit):
    # Checks each cell in the row and column of the given place
    for i in range(9):
        if (digit==sudoku_mat[row][i] or digit==sudoku_mat[i][col]):
            return 0

    # Checks each cell in the 3x3 square of the given place
    for i in range(3):
        for j in range(3):
            if (digit == sudoku_mat[(row//3)*3+i][(col//3)*3+j]):
                return 0
    # Return 1 if there are no collisions with the same digit
    return 1
"""
# Prints the two dimension array on the screen.
def print_puzzle(sudoku_mat):
    for i in range(9):
        for j in range(8):
            # Prints each cell of the matrix
            print(int(sudoku_mat[i][j]) , end=' ')
            if ((j+1)%3 == 0):	# prints a border every 3 columns
                print("|" , end=' ')
        # Prints the last number in a row and shifts to the next row
        print(int(sudoku_mat[i][8]) , end='\n')
        if ((i+1)%3==0 and i < 8):	# prints a border every 3 rows
            print("------+-------+------")
"""
