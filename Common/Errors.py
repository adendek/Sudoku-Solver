class InappropriateArgsError(Exception):
    def __init__(self, name):
        super().__init__("Inappropriate arguments when " + name + "!")


class AddingPointError(Exception):
    def __init__(self):
        super().__init__("Error when adding point to a square. It already has 4 points!")


class SudokuFieldSizeError(Exception):
    def __init__(self):
        super().__init__("The difference between width and height of the sudoku field is to big!")
