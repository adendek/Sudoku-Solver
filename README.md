# Sudoku-Solver
This program is designed to solve the [Sudoku puzzle](https://en.wikipedia.org/wiki/Sudoku), taken from the camera.
It uses [openCV](https://opencv.org/) library for sudoku field detection, and it uses [Backtracking](https://en.wikipedia.org/wiki/Backtracking) algorithm for saving it.

<img src="https://media1.giphy.com/media/QAuUc245sZHO/giphy.gif" width="200" height="200" />

Table of contents
=================
<!--ts-->
   * [Sudoku-Solver](#Sudoku-Solver)
   * [Table of contents](#Table-of-contents)
   * [Getting Started](#Getting-Started)
       * [Prerequisites](#Prerequisites)
       * [Quick start](#Quick-start)
   * [Tests](#Tests)
   * [Authors](#Authors)
<!--te-->
    
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### 1. Python

You need Python 3.4 or later to run Sudoku-Solver. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

`$ sudo apt-get install python3 python3-pip`

For other Linux flavors, OS X and Windows, packages are available at:

[http://www.python.org/getit/](http://www.python.org/getit/)

#### 2. Sudoku Solver
To get all of the files needed to run this program, decide for one of the following options and follow it's steps.

##### Using git
1. If the git is not yet installed, check this tutorial how to install it [https://www.atlassian.com/git/tutorials/install-git](https://www.atlassian.com/git/tutorials/install-git)
2. Open the console and go to the directory, where you want to download files.
3. Use the command `git clone https://github.com/ghribar97/Sudoku-Solver.git`.
4. Files are ready. To run Sudoku-Solver check [Quick start](#Quick start).

##### Download files
1. Go to the repository page [https://github.com/ghribar97/Sudoku-Solver](https://github.com/ghribar97/Sudoku-Solver)
2. Click a big green button "Clone or download" and choose "download ZIP" option.
3. After download you must unzip the files with a [WinZip](http://www.winzip.com/win/en/prod_down.html) software, or any other program.
4. Files are ready. To run Sudoku-Solver check [Quick start](#Quick start).

### Quick start

To start a program go to the directory where the Sudoku-Solver files are located and execute command:

`
$ python3 main.py
`

Afterthe execution the program should start.

## Tests
To run the tests for this project go to [Tests](https://github.com/ghribar97/Sudoku-Solver/tree/master/Tests) directory and run [mainTester.py](https://github.com/ghribar97/Sudoku-Solver/blob/master/Tests/mainTester.py)
Run it with this command:

`$ python3 mainTester.py`

Test coverage is:

[![Coverage Status](https://coveralls.io/repos/github/ghribar97/Sudoku-Solver/badge.svg?branch=master)](https://coveralls.io/github/ghribar97/Sudoku-Solver?branch=master)

## Authors
1. [Alexis Ouksel](https://github.com/AlexOUKS)
2. [Gašper Hribar](https://github.com/ghribar97)
3. [Jesus Prieto Garcia](https://github.com/jesusprietogarcia22)
4. [Roman Suchwalko](https://github.com/rsuchwalko)

[To the top!](#Sudoku-Solver)
