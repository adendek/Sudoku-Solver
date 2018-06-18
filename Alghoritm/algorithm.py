from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
import time

SIZE = 9


class SudokuSolver:
    #  function to print sudoku
    @staticmethod
    def print_sudoku(matrix):
        if Validator.is_9x9_integers_field(matrix):
            for i in matrix:
                print(i)

    #  function to check if all cells are assigned or not
    #  if there is any unassigned cell
    #  then this function will change the values of
    #  row and col accordingly
    @staticmethod
    def _number_unassigned(matrix):
        if Validator.is_9x9_integers_field(matrix):
            num_unassign = 0
            for i in range(0, SIZE):
                for j in range(0, SIZE):
                    if matrix[i][j] == 0:  # cell is unassigned
                        row = i
                        col = j
                        num_unassign = 1
                        a = [row,  col,  num_unassign]
                        return a
            a = [-1,  -1,  num_unassign]
            return a
        raise InappropriateArgsError("number unassigned")

    #  function to check if we can put a
    #  value in a particular cell or not
    @staticmethod
    def _is_safe(matrix, n,  r,  c):
        if Validator.is_9x9_integers_field(matrix) and \
                Validator.is_positive_number([n, r, c]) and Validator.is_type([n, r, c], int):  # positive integers
            #  checking in row
            for i in range(0, SIZE):
                #  there is a cell with same value
                if matrix[r][i] == n:
                    return False
            #  checking in column
            for i in range(0, SIZE):
                #  there is a cell with same value
                if matrix[i][c] == n:
                    return False
            row_start = (r // 3) * 3
            col_start = (c // 3) * 3
            #  checking submatrix
            for i in range(row_start, row_start+3):
                for j in range(col_start, col_start+3):
                    if matrix[i][j] == n:
                        return False
            return True
        raise InappropriateArgsError("checking if sudoku is save")
    
    #  function to check if we can put a
    #  value in a particular cell or not
    @staticmethod
    def _solve_sudoku(unsolved_matrix):
        if Validator.is_9x9_integers_field(unsolved_matrix):
            #  if all cells are assigned then the sudoku is already solved
            #  pass by reference because number_unassigned will change the values of row and col
            a = SudokuSolver._number_unassigned(unsolved_matrix)
            if a[2] == 0:
                return True
            row = a[0]
            col = a[1]
            #  number between 1 to 9
            for i in range(1, SIZE + 1):
                # if we can assign i to the cell or not
                # the cell is matrix[row][col]
                if SudokuSolver._is_safe(unsolved_matrix, i,  row,  col):
                    unsolved_matrix[row][col] = i
                    #  backtracking
                    if SudokuSolver._solve_sudoku(unsolved_matrix):
                        return True
                    # if we can't proceed with this solution
                    # reassign the cell
                    unsolved_matrix[row][col] = 0
            return False
        raise InappropriateArgsError("solving sudoku")

    @staticmethod
    def get_solution(unsolved_matrix, print_solution=False):
        if Validator.is_9x9_integers_field(unsolved_matrix):
            solution = SudokuSolver._solve_sudoku(unsolved_matrix)
            if solution:
                if print_solution:
                    SudokuSolver.print_sudoku(unsolved_matrix)
                return unsolved_matrix
            if print_solution:
                print("No solution!")
            return False  # can not solve sudoku
        raise InappropriateArgsError("getting solution for sudoku field")

    @staticmethod
    def get_execution_time(unsolved_matrix):
        start_time = time.time()
        SudokuSolver.get_solution(unsolved_matrix)
        exec_time = time.time() - start_time
        print("\n\n--- %s seconds ---\n" % exec_time)
        return exec_time
    

if __name__ == '__main__':
    legit_matrix = [
        [6, 5, 0, 8, 7, 3, 0, 9, 0], 
        [0, 0, 3, 2, 5, 0, 0, 0, 8], 
        [9, 8, 0, 1, 0, 4, 3, 5, 7], 
        [1, 0, 5, 0, 0, 0, 0, 0, 0], 
        [4, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 1, 0, 5, 0, 3],
        [5, 7, 8, 3, 0, 1, 0, 2, 6],
        [2, 0, 0, 0, 4, 8, 9, 0, 0],
        [0, 9, 0, 6, 2, 5, 0, 8, 1]
    ]
    unsolvable_matrix = [
        [1, 2, 0, 4, 5, 6, 7, 8, 9],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    wrong_matrix = [
        [1, 2, 0, 4, 5, 6, 7, 8, 9],
        [0, 0, 3, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    hard_matrix = [
        [0, 6, 1, 0, 0, 7, 0, 0, 3],
        [0, 9, 2, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 5, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 4],
        [5, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 6, 0, 8, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    print("legit matrix:")
    SudokuSolver.get_solution(legit_matrix, print_solution=True)
    print("unsolvable matrix:")
    SudokuSolver.get_solution(unsolvable_matrix, print_solution=True)
    print("wrong matrix:")
    SudokuSolver.get_solution(wrong_matrix, print_solution=True)
    # SudokuSolver.get_execution_time(hard_matrix)  # 834.57s  -  14 min o.O
