from GUI.Framework import sudokuFieldTemplate
from GUI import solutionView


class AskIfCorrectView(sudokuFieldTemplate.SudokuFieldTemplate):
    def __init__(self, field, loaded_from):
        super().__init__("It is correct", self._go_to_solution, field, loaded_from)
        self.mainloop()

    def _get_current_field(self):
        field = [
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
        ]
        return field

    def _go_to_solution(self):
        self.withdraw()
        solutionView.SolutionView(self._get_current_field(), self)
