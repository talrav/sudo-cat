  
  
# SudoCat Project
  
  Grumpy cat has mastered Sudoku in heaven. Now he is back to solve your Sudoku puzzles!  
  
  The following repository include a Sudoku puzzle game. The game interface consist of three main options:  
  <img src="https://i.imgur.com/vuvEqME.gif" alt="Gcat_MI" height="200" align="right" title="mehh"/>  
  
  1.  **Player game mode** - Enable playing a random Sudoku game from a database of 10,000 different puzzles.  
  1.  **Recursive solver** - show an example of how to solve the current puzzle using a recursive method.  
  1.  **CNN solver** - Provide a solution to the current puzzle using a trained CNN algorithm. The network learned from a database of 100,000 different puzzles and solutions.  
  
  Each solved puzzle can be verified by its own solution provided by the database.
  
  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat1" width="30" title="too easy"/>  How to play
  
  First, download the whole repository to a folder. Then locate the file ['gui_sudoku.py'](https://github.com/Tal-Raveh/SudoCat/blob/master/gui_sudoku.py "'gui_sudoku.py'") and run it using any python console.
  
  That's it, you are ready to play SudoCat! Be sure to check the different options...  
  
  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat2" width="30"  title="boring"/>  Player game mode
  
  Player mode is the defualt mode, it means you can write a number in each cell and check if you got it right.
  If you get it wrong, you get an error messege:
  
  <img src="https://github.com/Tal-Raveh/SudoCat/blob/master/example1.png" alt="Gcat_ex" width="500" title="example"/>  
  
  

##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat3" width="30"  title="did that too... and i'm a cat"/>  Recursive solver
  
  Recursive method to solve any Sudoku puzzle:  
  ![Recursive example](https://upload.wikimedia.org/wikipedia/commons/8/8c/Sudoku_solved_by_bactracking.gif "Recursive example")

The file responsible for this section - ['recursive_solver.py'](https://github.com/Tal-Raveh/SudoCat/blob/master/recursive_solver.py "'recursive_solver.py'").

  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat4" width="30" title="still not impressed"/>  CNN solver
  
  We created a model with 2 dense layer's plus a dense layer for each cell in the sudoku (2 + 81 = 83 in total).
  We trained the model over 100,000 sudokus and 10 epochs.
  We got 99% correct sudokus over 10,000 testing data (data = sudokus):
  
  <img src="https://github.com/Tal-Raveh/SudoCat/blob/master/solved_10000.png" alt="Cnn1" width="200" title="CNN testing percentage"/>
  
  If you want to load our trained model and test it:
  1.  Download the whole repository to a folder.
  1.  Unzip ['sudoku_trained-100000.part1.rar'](https://github.com/Tal-Raveh/SudoCat/blob/master/sudoku_trained-100000.part1.rar "'sudoku_trained-100000.part1.rar'") and ['sudoku_trained-100000.part2.rar'](https://github.com/Tal-Raveh/SudoCat/blob/master/sudoku_trained-100000.part2.rar "'sudoku_trained-100000.part2.rar'") to the main folder.
  1.  Run "main_cnn.py".
 
  If you want to train the model all you need to do is:
  1.  Download the whole repository to a folder.
  1.  Change the num_train_data and num_test_data as you wish.
  1.  Open the file ['main_cnn.py'](https://github.com/Tal-Raveh/SudoCat/blob/master/main_cnn.py "'main_cnn.py'") and make sure to uncomment "solver = train(...)", **line 91**.
  1.  Uncomment "solver.save(NAME)", **line 95** (Not obligatory, do it only if you want to save the model).
  1.  Comment **line 98**, this line loads our model.
  
  **FYI : All the solved sudokus by the CNN model were saved in a csv file, so when you press solve, you get the solution from the csv file. We made it that way only to speed up the program.**
