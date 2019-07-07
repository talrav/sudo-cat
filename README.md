  
  
# SudoCat Project
  
  Grumpy cat has mastered Sudoku in heaven. Now he is back to solve your Sudoku puzzles!  
  
  The following repository include a Sudoku puzzle game. The game interface consist of three main options:  
  <img src="http://jasperboerstra.nl/____impro/1/onewebmedia/stickertapinorder.gif?etag=W%2F%2216380-58bd8036%22&sourceContentType=image%2Fgif" alt="Gcat_MI" height="200" align="right" title="mehh"/>  
  
  1.  **Player game mode** - Enable playing a random Sudoku game from a database of 10,000 different puzzles.  
  1.  **Recursive solver** - show an example of how to solve the current puzzle using a recursive method.  
  1.  **CNN solver** - Provide a solution to the current puzzle using a trained CNN algorithm. The network learned from a database of 100,000 different puzzles and solutions.  
  
  Each solved puzzle can be verified by its own solution provided by the database.
  
  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat1" width="30" title="too easy"/>  How to play
  
  First, download the whole repository to a folder. then locate the file ['gui_sudoku.py'](https://github.com/Tal-Raveh/SudoCat/blob/master/gui_sudoku.py "'gui_sudoku.py'") and run it using any python console.
  
  That's it, you are ready to play SudoCat! Be sure to check the different options
  
  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat2" width="30"  title="boring"/>  Player game mode
  
  Banana
  
  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat3" width="30"  title="did that too... and i'm a cat"/>  Recursive solver
  
  Recursive method to solve any Sudoku puzzle:  
  ![Recursive example](https://upload.wikimedia.org/wikipedia/commons/8/8c/Sudoku_solved_by_bactracking.gif "Recursive example")
  
  
##   <img src="https://d2rd7etdn93tqb.cloudfront.net/wp-content/uploads/2015/02/6-grumpy-cat.jpg" alt="Gcat4" width="30" title="still not impressed"/>  CNN solver
  
  We created a model with 2 dense layer's plus a dense layer for each cell in the sudoku (2 + 81 = 83 in total).
  We got 99% correct sudokus over 10,000 testing data:
  <img src="https://github.com/Tal-Raveh/SudoCat/blob/master/solved_10000.png" alt="Cnn1" width="150" title="CNN testing percentage"/>
  
