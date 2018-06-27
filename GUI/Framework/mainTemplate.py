from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
import GUI.Framework.widgets as widgets
import GUI.Variables.variables as var
import tkinter
import sys


class MainTemplate(tkinter.Tk):
    def __init__(self, bt1_text, bt1_funct, bt2_text, bt2_funct):
        if Validator.is_type([bt1_text, bt2_text], str) and Validator.is_function([bt1_funct, bt2_funct]):
            super().__init__()
            self.title(var.TITLE_TEXT)

            self.title_frame = widgets.Frame(self, row=1, padx=var.BORDER, pady=var.BORDER)
            self.title_label = widgets.Title(self.title_frame, var.TITLE_TEXT)

            self.info_frame = widgets.Frame(self, row=3, padx=var.BORDER, pady=var.BORDER)
            self.info_label = widgets.Label(self.info_frame, "")

            self.bot_frame = widgets.Frame(self, row=4, sticky="ew", padx=var.BORDER, pady=var.BORDER)
            self.bot_frame.grid_columnconfigure(0, weight=1)
            self.bot_frame.grid_columnconfigure(1, weight=1)

            self.left_button_frame = widgets.Frame(self.bot_frame, row=0, column=0, sticky="w")
            self.right_button_frame = widgets.Frame(self.bot_frame, row=0, column=1, sticky="e")

            self.left_button = widgets.Button(self.left_button_frame, bt1_text, bt1_funct)
            self.right_button = widgets.Button(self.right_button_frame, bt2_text, bt2_funct)

            self.protocol("WM_DELETE_WINDOW", self._on_destroy)
            self.resizable(False, False)
        else:
            raise InappropriateArgsError("a main template!")

    def set_info_label(self, text):
        if Validator.is_type(text, str):
            self.info_label.config(fg="black")
            self.info_label["text"] = text
            return text
        else:
            raise InappropriateArgsError("setting info label text!")

    def display_error(self, text, after_error_text, error_duration):
        if Validator.is_type([text, after_error_text], str) and Validator.is_positive_number(error_duration):
            self.info_label.config(fg="red")
            self.set_info_label(text)
            self.after(error_duration, lambda: self.set_info_label(after_error_text))
            return text
        else:
            raise InappropriateArgsError("setting info label text!")

    def _get_window_size(self):
        return self.winfo_width(), self.winfo_height()

    def _calculate_middle(self, width, height):
        if Validator.is_positive_number([width, height]):
            return (self.winfo_screenwidth() // 2) - (width // 2), (self.winfo_screenheight() // 2) - (height // 2)
        raise InappropriateArgsError("calculating center of the screen!")

    def _set_to_screen_center(self):
        self.update_idletasks()
        width, height = self._get_window_size()
        x, y = self._calculate_middle(width, height)
        self.geometry('+{}+{}'.format(x, y - 40))

    def _on_destroy(self):
        tkinter._default_root = self
        self.destroy()
        sys.exit(0)
