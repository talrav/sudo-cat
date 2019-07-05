import sys
from tempfile import NamedTemporaryFile
from time import time
from os.path import dirname, join
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# from logic import SolveSudokuPuzzle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from load_data import load_data
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from recursive_solver import solve_sudoku_rec, possible

def fun(n_rows, n_columns):
    return [[QColor(qrand() % 256, qrand() % 256, qrand() % 256) for i in range(n_rows)] for j in range(n_columns)]


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'SudoCat'
        self.left = 200
        self.top = 200
        self.width = 760
        self.height = 540
        self.rand_game = 1
        self.xgame = []
        self.ygame = []
        self.box_size = 50
        self.which_solution_flag = 'me'   # ['me', 'recursion', 'cnn']
        self.initUI()

    # def addButton(self, name):
    #     button = QPushButton(name, self)
    #     button.setToolTip('This is an example button')
    #     button.move(650, 10)
    #     button.clicked.connect(self.on_click)
    #     button.resize(150, 32)

    def initUI(self):
        hbox = QHBoxLayout(self)
        SudokuGrid = QFrame(self)
        SudokuGrid.setFrameShape(QFrame.StyledPanel)
        # SudokuGrid.setStyleSheet("background-image: url(grumpy-cat.jpg)")

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(SudokuGrid)
        splitter1.addWidget(right)
        splitter1.setSizes([1])

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)


        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('grumpy-cat.jpg'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        button = QPushButton('New Game', self)
        button.setToolTip('Start new game')

        x_pos_buttons = self.box_size*9 + 100
        y_pos_buttons_start = 40
        y_pos_buttons_diff = 45

        button.move(x_pos_buttons, y_pos_buttons_start + y_pos_buttons_diff*0)
        button.clicked.connect(self.on_click_new_game)
        button.resize(150, 32)
        button.setStyleSheet("background-color: #A3C1DA")

        button = QPushButton("Recursive Solver", self)
        button.setToolTip('Solve the sudoku with recursion')
        button.move(x_pos_buttons, y_pos_buttons_start + y_pos_buttons_diff*1)
        button.clicked.connect(self.on_click_recursive_solver)
        button.resize(150, 32)
        button.setStyleSheet("background-color: #A3C1DA")


        button = QPushButton("CNN Solver", self)
        button.setToolTip('Solve the sudoku with CNN')
        button.move(x_pos_buttons, y_pos_buttons_start + y_pos_buttons_diff*2)
        button.clicked.connect(self.on_click_cnn_solver)
        button.resize(150, 32)
        button.setStyleSheet("background-color: #A3C1DA")

        button = QPushButton("Clear", self)
        button.setToolTip('clear sudoku')
        button.move(x_pos_buttons, y_pos_buttons_start + y_pos_buttons_diff*3)
        button.clicked.connect(self.on_click_clear)
        button.resize(150, 32)
        button.setStyleSheet("background-color: #A3C1DA")

        button = QPushButton("Check", self)
        button.setToolTip('Checks current solution')
        button.move(x_pos_buttons, y_pos_buttons_start + y_pos_buttons_diff*4)
        button.clicked.connect(self.on_click_check)
        button.resize(150, 32)
        button.setStyleSheet("background-color: #A3C1DA")

        font = QFont()
        font.setBold(True)
        self.table = QTableWidget(SudokuGrid)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.table.setRowCount(9)
        self.table.setColumnCount(9)

        for i in range(9):
            self.table.setColumnWidth(i, self.box_size)
        for i in range(9):
            self.table.setRowHeight(i, self.box_size)

        # self.table.resizeColumnsToContents()
        # self.table.resize(524, 407)
        self.table.resize(self.box_size*9 + 4, self.box_size*9 + 4)
        self.table.move(35,30)
        self.table.setFont(font)
        self.table_color()

        self.show()

    def table_color(self):
        for row in range(9):
            if(row<3):
                for col in range(9):
                    if (col<3):
                        self.table.setItem(row,col, QtWidgets.QTableWidgetItem())
                        self.table.item(row,col).setBackground(QColor("#A3C1DA"))
                    if (col>5):
                        self.table.setItem(row,col, QtWidgets.QTableWidgetItem())
                        self.table.item(row,col).setBackground(QColor("#A3C1DA"))
            if (row > 5):
                for col in range(4):
                    if (col<3):
                        self.table.setItem(row-3,col+3, QtWidgets.QTableWidgetItem())
                        self.table.item(row-3,col+3).setBackground(QColor("#A3C1DA"))
                for col in range(9):
                    if (col < 3):
                        self.table.setItem(row, col, QtWidgets.QTableWidgetItem())
                        self.table.item(row, col).setBackground(QColor("#A3C1DA"))
                    if (col > 5):
                        self.table.setItem(row, col, QtWidgets.QTableWidgetItem())
                        self.table.item(row, col).setBackground(QColor("#A3C1DA"))

        self.table.setStyleSheet("selection-background-color: blue;")
    
    def on_click(self):
        print('PyQt5 button click')

    def on_click_new_game(self):
        self.which_solution_flag = 'me'
        self.rand_game = np.random.randint(10000)+1
        (self.xgame, self.ygame) = load_data(file_name='sudoku_games.csv', spec_sudoku=self.rand_game)
        main = [w for w in QApplication.topLevelWidgets() if isinstance(w, App)][0]
        main.table_add_item(str(self.xgame))

    def on_click_recursive_solver(self):
        self.which_solution_flag = 'recursive'
        sudoku_mat_rec = solve_sudoku_rec(self.xgame[0] , 0 , 0)
        main = [w for w in QApplication.topLevelWidgets() if isinstance(w, App)][0]
        main.table_add_item(str(sudoku_mat_rec))

    def on_click_cnn_solver(self):
        self.which_solution_flag = 'cnn'
        (_, sudoku_mat_cnn) = load_data(file_name='keras_solutions.csv', spec_sudoku=self.rand_game)
        # sudoku_mat_cnn = solve_sudoku_cnn(self.xgame)
        main = [w for w in QApplication.topLevelWidgets() if isinstance(w, App)][0]
        main.table_add_item(str(sudoku_mat_cnn))
       

    def on_click_clear(self):
        self.which_solution_flag = 'me'
        main = [w for w in QApplication.topLevelWidgets() if isinstance(w, App)][0]
        self.table.clearContents()
        self.table_color()
    
    def on_click_check(self):
        current_solution = []
        for i in range(9):
            for j in range(9):
                if self.table.item(i, j).text() == ' ':
                    current_solution = np.append(
                        current_solution, 0)
                    continue
                current_solution = np.append(
                    current_solution, int(self.table.item(i, j).text()))
        
        check_81 = (current_solution == self.ygame.reshape(-1)).sum()

        if self.which_solution_flag == 'recursive':
            if check_81 == 81:
                self.msg("Recursive solution", "Recursive solution is true!", "happy_cat.png")
            else:
                self.msg("Recursive solution",
                         "Recursive solution is false!", "grampy_cat.png")
        if self.which_solution_flag == 'cnn':
            if check_81 == 81:
                self.msg("CNN solution",
                         "CNN solution is true!", "happy_cat.png")
            else:
                self.msg("CNN solution",
                         "CNN solution is false!", "grampy_cat.png")
        if self.which_solution_flag == 'me':
            if check_81 == 81:
                self.msg("Your solution",
                         "Your solution is true!", "happy_cat.png")
            else:
                self.msg("Your solution",
                         "Your solution is false!", "grampy_cat.png")

    def table_add_item(self, items):
        string = ''.join([str(x) for x in items])
        # print(str(items).strip('[]'))
        items = items.replace(' ', '')
        items = items.replace('[', '')
        items = items.replace(']', '')
        items = items.replace('\n', '')
        items = items.replace('0', ' ')
        for i, text in enumerate(items):
            self.table.setItem(0, i, QTableWidgetItem(text))
            for row in range(9):
                if (row < 3):
                    for col in range(9):
                        if (col < 3):
                            self.table.setItem(0, i, QtWidgets.QTableWidgetItem(text))
                            self.table.item(row, col).setBackground(QColor("#A3C1DA"))
                        if (col > 5):
                            self.table.setItem(0, i, QtWidgets.QTableWidgetItem(text))
                            self.table.item(row, col).setBackground(QColor("#A3C1DA"))
                if (row > 5):
                    for col in range(4):
                        if (col < 3):
                            self.table.setItem(0, i, QtWidgets.QTableWidgetItem(text))
                            self.table.item(row - 3, col + 3).setBackground(QColor("#A3C1DA"))
                    for col in range(9):
                        if (col < 3):
                            self.table.setItem(0, i, QtWidgets.QTableWidgetItem(text))
                            self.table.item(row, col).setBackground(QColor("#A3C1DA"))
                        if (col > 5):
                            self.table.setItem(0, i, QtWidgets.QTableWidgetItem(text))
                            self.table.item(row, col).setBackground(QColor("#A3C1DA"))

            self.table.setStyleSheet("selection-background-color: blue;")
    
    def msg(self, title, txt, image_name):
        image_path = "data\images\\"
        messagebox = QMessageBox(
            QMessageBox.Warning, title, txt)
        messagebox.setDefaultButton(QMessageBox.Cancel)
        messagebox.setIconPixmap(QPixmap(image_path + image_name))
        exe = messagebox.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()
    sys.exit(app.exec_())
