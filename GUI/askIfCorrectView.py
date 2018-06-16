from GUI.Framework import sudokuFieldTemplate
from GUI import solutionView
from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError


class AskIfCorrectView(sudokuFieldTemplate.SudokuFieldTemplate):
    def __init__(self, field, loaded_from):
        if Validator.is_9x9_integers_field(field):
            super().__init__("Continue", self._go_to_solution, field, loaded_from)
            self.set_info_label("If the numbers are matching press 'Continue',\n else manually change the wrong ones.")
        else:
            raise InappropriateArgsError("creating error handling view (AskIfCorrectView)!")

    def _get_current_field(self):
        for y, row in enumerate(self.text_edits):
            for x, text_edit in enumerate(row):
                value = text_edit.get_value()
                if value == "":
                    self.field_numbers[y][x] = 0
                else:
                    self.field_numbers[y][x] = int(text_edit.get_value())
        return self.field_numbers

    def _go_to_solution(self):
        self.withdraw()
        solutionView.SolutionView(self._get_current_field(), self)