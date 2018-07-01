class InappropriateArgsError(Exception):
    def __init__(self, name):
        super().__init__("Inappropriate arguments when " + str(name) + "!")


class SudokuFieldSizeError(Exception):
    def __init__(self):
        super().__init__("The difference between width and height of the sudoku field is to big!")
