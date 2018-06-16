from GUI.Framework import sudokuFieldTemplate
from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError


class SolutionView(sudokuFieldTemplate.SudokuFieldTemplate):
    def __init__(self, field, loaded_from):
        if Validator.is_9x9_integers_field(field):
            super().__init__("Change Digits", self._go_to_correct, field, loaded_from, readonly=True)
            self.set_info_label("This is the solution to the given sudoku!")
        else:
            raise InappropriateArgsError("creating solution View!")

    def _go_to_correct(self):
        self.destroy()
        self.loaded_from.deiconify()  # makes window visible again

    def _go_back(self):
        self.loaded_from.destroy()
        self.loaded_from = self.loaded_from.loaded_from
        super()._go_back()
