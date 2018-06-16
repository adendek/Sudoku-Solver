from GUI.Framework import sudokuFieldTemplate


class SolutionView(sudokuFieldTemplate.SudokuFieldTemplate):
    def __init__(self, field, loaded_from):
        super().__init__("Take another picture", self._go_to_correct, field, loaded_from, readonly=True)

    def _go_to_correct(self):
        self.destroy()
        self.loaded_from.deiconify()  # makes window visible again

    def _go_back(self):
        self.loaded_from.destroy()
        self.loaded_from = self.loaded_from.loaded_from
        super()._go_back()
