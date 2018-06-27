from GUI.Framework import sudokuFieldTemplate
from GUI import solutionView
from GUI.Variables.variables import ICON_PATH
from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
from Alghoritm.algorithm import SudokuSolver
from GUI.Framework import widgets


class AskIfCorrectView(sudokuFieldTemplate.SudokuFieldTemplate):
    def __init__(self, field, loaded_from):
        if Validator.is_9x9_integers_field(field):
            super().__init__("Continue", self._go_to_solution, field, loaded_from)
            self.label_text = "If the numbers are matching press 'Continue',\n else manually change the wrong ones."
            self.set_info_label(self.label_text)
            show_image_frame = widgets.Frame(self.bot_frame, row=0, column=1, sticky="w")
            self.show_image_button = widgets.Button(show_image_frame, "Show field", self._show_detected_field)
        else:
            raise InappropriateArgsError("creating error handling view (AskIfCorrectView)!")

    def _show_detected_field(self):
        process = self.loaded_from.process
        process.draw_grid()
        process.show_field()

    def _get_current_field(self):
        detected = []
        for y, row in enumerate(self.text_edits):
            for x, text_edit in enumerate(row):
                value = text_edit.get_value()
                if value == "":
                    self.field_numbers[y][x] = 0
                else:
                    detected.append(y * 9 + x)
                    self.field_numbers[y][x] = int(text_edit.get_value())
        return SudokuSolver.get_solution(self.field_numbers), detected

    def _go_to_solution(self):
        msg = self.display_message("Processing...\n", self.label_text, "green", 1)
        self.update_idletasks()
        solution, detected = self._get_current_field()
        self.after_cancel(msg)
        self.set_info_label(self.label_text)
        self.withdraw()
        if solution:
            view = solutionView.SolutionView(solution, detected, self)
        else:
            text = "There is no solution to this sudoku!"
            view = solutionView.SolutionView(self.field_numbers, detected,  self, text=text)
        view.iconbitmap(ICON_PATH)
