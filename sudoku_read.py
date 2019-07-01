"""
~SudoCat~

Recursive Sudoku Solver
"""

import numpy as np
import time
import pickle
import random

# Read the csv data file containing 1,000,000 sudoku quizzes with their solution 
# and builds a data structure containing the input-output examples in "sudoku_data.sqs".
def read_csv():
    # Check the run time elapsed
    s_time = time.time()                        # start the timer
    # Open the file and start reading
    with open("sudoku_data.csv" , "r") as csv_file:
        quizzes = np.zeros((1000000,9,9))             # init the empty quizzes matrix
        solutions = np.zeros((1000000,9,9))           # init the full solutions matrix
        print("Loading patterns from sudoku_data.csv...")
        # Read each pattern
        for idx, line in enumerate(csv_file):
            if (idx > 0):
                if (idx%100000 == 0):
                    print("Read %3d%% after %.2f seconds" %((idx/1000000)*100 , time.time()-s_time))
                for i in range(9):
                    for j in range(9):
                        quizzes[idx-1][i][j] = line[i+9*j]
                        solutions[idx-1][i][j] = line[82+i+9*j]
        f_time = time.time()                    # end the timer
    print("Done reading 1000000 patterns in %.2f minutes" %((f_time-s_time)/60))
    saver("sudoku_data.sqs", (quizzes , solutions))

# Saves the puzzle database to a file 
def saver(file_name , data):
    try:
        with open(file_name , "wb") as file:
            pickle.dump(data , file)
    except EnvironmentError:
        print("Something went wrong while writing to the file '%s'." %(file_name))

# Loads the puzzle database from a file
def loader(file_name):
    try:
        with open(file_name , "rb") as file:
            return pickle.load(file)
    except EnvironmentError:
        print("Couldn't find the file '%s' in the directory." %(file_name))
        return 0,0

# Solving the sudoku puzzle using a recursive method and returns the solved matrix
def solve_sudoku(sudoku_mat , row , col):
    # End condition of the recursion, if the solution got to row 9 - the matrix is full
    if (row > 8):
        return sudoku_mat
    
    if sudoku_mat[row][col]:            # if a cell is already filled - skip it
        if (col < 8):                   # is it possible to shift to the next column?
            # call the function to check the next cell
            if solve_sudoku(sudoku_mat , row , col+1)[0][0]:
                # if the next cell returned a value, this cell will return to the prior cell a value
                return sudoku_mat
        elif solve_sudoku(sudoku_mat , row+1 , 0)[0][0]:      # shifts to the next row
            return sudoku_mat
        # if the next cell returned 0, this cell will return to the prior cell 0
        return [[0]]
    
    for digit in range(1,10):
        # run over the numbers possible for this empty cell
        if possible(sudoku_mat , row , col , digit):
            sudoku_mat[row][col] = digit	# if its possible to insert the number - put it in
            
            if (col < 8):	# shifts to the next cell
                if solve_sudoku(sudoku_mat , row , col+1)[0][0]:
                    return sudoku_mat
            elif solve_sudoku(sudoku_mat , row+1 , 0)[0][0]:
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

def main():
    #read_csv()
    quizzes , solutions = loader("sudoku_data.sqs")
    
    game = int(input("Please insert a game number (0 to choose randomly): "))
    if (game<1 or game>1000000):
        game = random.randint(1,1000001)
    sol = solutions[game]
    sudoku_mat = quizzes[game]
    
    del quizzes , solutions
    
    print("\nThe chosen one (#%d):" %(game))
    print_puzzle(sudoku_mat)
    print("\nThe known solution (#%d):" %(game))
    print_puzzle(sol)
    sudoku_mat = solve_sudoku(sudoku_mat , 0 , 0)
    print("\nThe recursive solution:")
    print_puzzle(sudoku_mat)

    print("\nComparing the two solutions:")
    if (sudoku_mat == sol).all():
        print("\tThe recursive solution is EQUAL to the given solution!")
    else:
        print("\tThe recursive solution is NOT the same as the given solution!")
    
    return sudoku_mat , sol

if __name__ == "__main__":
    game , sol = main()
    
