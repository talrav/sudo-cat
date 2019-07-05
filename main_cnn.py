# imports
import numpy as np

from keras import Model, Sequential
from keras.callbacks import TensorBoard
from keras.layers import Dense, Dropout, Flatten, Input
from keras.utils import to_categorical
from keras.models import load_model

from load_data import load_data
from diff import diff
from batch_solver import batch_solve
from write_to_csv import write_csv

def train(Xtrain, ytrain, Xtest, ytest):

    tensorboard = TensorBoard(log_dir='logs_new/')

    input_shape = (9, 9, 10)
    # We won't use _. We will work directly with ytrain

    # one-hot-encoding --> shapes become :
    # (?, 9, 9, 10) for Xs
    # (?, 9, 9, 9) for ys
    Xtrain = to_categorical(Xtrain).astype('float32')
    Xtest = to_categorical(Xtest).astype('float32')
    # (y - 1) because we don't want to predict zeros
    ytrain = to_categorical(ytrain-1).astype('float32')
    ytest = to_categorical(ytest-1).astype('float32')

    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dropout(rate=0.4))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(rate=0.4))
    model.add(Flatten())

    grid = Input(shape=input_shape)  # inputs
    features = model(grid)  # commons features
    # define one Dense layer for each of the digit we want to predict
    digit_placeholders = [Dense(9, activation='softmax')(
        features) for i in range(81)]
    solver = Model(grid, digit_placeholders)  # build the whole model
    solver.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    solver.fit(
        Xtrain,
        [ytrain[:, i, j, :] for i in range(9) for j in range(9)],
        validation_split=(0.1),
        batch_size=128,
        epochs=10,
        verbose=0,
        callbacks=[tensorboard]
    )
    
    return solver


def test(solver, quizzes, true_grids):
    
    solved_sudoku = batch_solve(quizzes, solver)  # make guesses

    deltas = diff(true_grids, solved_sudoku) # get number of errors on each quizz
    accuracy = (deltas == 0).mean()  # portion of correct solved quizzes

    print(
        """
    Grid solved:\t {}
    Correct ones:\t {}
    Accuracy:\t {}
    """.format(
            deltas.shape[0], (deltas == 0).sum(), accuracy
        )
    )

    return solved_sudoku


def main():
    # Reads data
    num_train_data = 100000
    num_test_data = 10000
    (Xtrain, ytrain), (Xtest, ytest) = load_data(
        num_train_data, num_test_data, file_name='sudoku_learn_data.csv')

    # Solving using CNN
    # solver = train(Xtrain, ytrain, Xtest, ytest)

    # Save's the traind model
    # NAME = "sudoku_trained-{}.model".format(str(len(Xtrain)))
    # solver.save(NAME)

    # Load's the traind model
    solver = load_model('sudoku_trained-100000.model')

    # Testing the trained model
    solved_sudokus = test(solver, Xtest, ytest)

    # Writes the test resaults to a csv file
    # write_csv(Xtest, solved_sudokus)


if __name__ == "__main__":
    main()
