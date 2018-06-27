import GUI.Framework.mainTemplate as mainTemplate
import GUI.Framework.widgets as widgets
import GUI.Variables.variables as var
from Common.Errors import InappropriateArgsError
from Common.validationFunctions import Validator
import tkinter


class SudokuFieldTemplate(mainTemplate.MainTemplate):
    def __init__(self, bt_text, bt_funct, field_numbers, loaded_from, readonly=False, detected=None):
        """
        creates a template with Sudoku field.
        :param bt_text: text of the button
        :param bt_funct: function of the button
        :param field_numbers: numbers that are in the field... 2d array with 9 elements each
        """
        if Validator.is_type(bt_text, str) and Validator.is_function(bt_funct) and \
                Validator.is_type(readonly, bool) and Validator.is_9x9_integers_field(field_numbers):
            tkinter._default_root = self
            super().__init__("Go Back", self._go_back, bt_text, bt_funct)
            self.content_frame = widgets.Frame(self, row=2, padx=var.BORDER, pady=var.BORDER)
            self.field_numbers = field_numbers  # 2d list of input digits
            self.readonly = readonly
            self.loaded_from = loaded_from
            self.detected = detected  # non empty fields (from original field)
            if self.detected is None:
                self.detected = []
            self.text_edits = self._generate_field()  # 2d list of entries

            self._set_to_screen_center()
        else:
            raise InappropriateArgsError("creating a sudoku field template!")

    def _generate_field(self):
        text_edits = []
        for y, row in enumerate(self.field_numbers):  # sudoku field is 9x9
            line = []
            for x, number in enumerate(row):
                text_edit = widgets.TextEdit(self.content_frame, number, readonly=self.readonly, row=y, column=x)
                if (len(self.detected) == 0 and number != 0) or (y * 9 + x) in self.detected:
                    text_edit.config(background="gray93")
                    text_edit.config(readonlybackground="gray85")
                line.append(text_edit)
            text_edits.append(line)
        return text_edits

    def _go_back(self):
        self.destroy()
        tkinter._default_root = self.loaded_from
        self.loaded_from.load_video()
        self.loaded_from.deiconify()  # makes window visible again

    def _on_destroy(self):
        self.loaded_from.destroy()
        super()._on_destroy()
