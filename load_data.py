import pandas as pd
import numpy as np
import os

def load_data(n_train=100000, n_test=10000, file_name='sudoku_learn_data.csv', spec_sudoku=0):
    """
    Function to load data in the keras way.

    Parameters
    ----------
    n_train (int): Number of training examples
    n_test (int): Number of testing examples

    Returns
    -------
    Xtrain, ytrain (np.array, np.array),
        shapes (nb_train, 9, 9), (nb_train, 9, 9): Training samples
    Xtest, ytest (np.array, np.array),
        shapes (nb_test, 9, 9), (nb_test, 9, 9): Testing samples
    """
    filepath = os.path.join("data/", file_name)

    if spec_sudoku is not 0:
        sudokus = next(pd.read_csv(filepath, skiprows=(spec_sudoku), chunksize=(1))).values
    else:
        sudokus = next(pd.read_csv(filepath, chunksize=(n_train + n_test))).values

    quizzes, solutions = sudokus.T
    flatX = np.array([np.reshape([int(d) for d in flatten_grid], (9, 9))
                      for flatten_grid in quizzes])
    flaty = np.array([np.reshape([int(d) for d in flatten_grid], (9, 9))
                      for flatten_grid in solutions])
    if spec_sudoku is not 0:
        return (flatX[:], flaty[:])
    else:
        return (flatX[:n_train], flaty[:n_train]), (flatX[n_train:], flaty[n_train:])
