import numpy as np

from keras.utils import to_categorical


def batch_solve(grids, solver):
    """
    This function solves quizzes in the "smart" way.
    It will fill blanks one after the other. Each time a digit is filled,
    the new grid will be fed again to the solver to predict the next digit.
    Again and again, until there is no more blank

    Parameters
    ----------
    grids (np.array), shape (?, 9, 9): Batch of quizzes to solve (smartly ;))
    solver (keras.model): The neural net solver

    Returns
    -------
    grids (np.array), shape (?, 9, 9): Smartly solved quizzes.
    """
    grids = grids.copy()
    for _ in range((grids == 0).sum((1, 2)).max()):
        preds = np.array(solver.predict(
            to_categorical(grids)))  # get predictions
        # get highest probability for each 81 digit to predict
        probs = preds.max(2).T
        values = preds.argmax(2).T + 1  # get corresponding values
        zeros = (grids == 0).reshape(
            (grids.shape[0], 81))  # get blank positions

        for grid, prob, value, zero in zip(grids, probs, values, zeros):
            if any(zero):  # don't try to fill already completed grid
                where = np.where(zero)[0]  # focus on blanks only
                # best score FOR A ZERO VALUE (confident blank)
                confidence_position = where[prob[zero].argmax()]
                # get corresponding value
                confidence_value = value[confidence_position]
                # fill digit inplace
                grid.flat[confidence_position] = confidence_value
    return grids
