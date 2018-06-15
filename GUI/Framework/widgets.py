import tkinter
import GUI.variables.variables as var
from Common.validationFunctions import Validator


class Frame(tkinter.Frame):
    def __init__(self, parent, height=10, width=10, **kwargs):
        if Validator.is_positive_number([height, width]) and \
                (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)):
            super().__init__(master=parent, height=height, width=width)
            self.grid(kwargs)
        else:
            raise ValueError("Inappropriate arguments when creating a frame!")


class Button(tkinter.Button):
    def __init__(self, parent, text, action, **kwargs):
        if (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)) \
                and Validator.is_type(text, str) and Validator.is_function(action):
            super().__init__(master=parent, text=text, command=action, width=10)
            self.config(bg=var.BUTTON_BACKGROUND, fg=var.BUTTON_TEXTCOLOR)
            self.grid(kwargs)
        else:
            raise ValueError("Inappropriate arguments when creating a button!")


class Label(tkinter.Label):
    def __init__(self, parent, text, **kwargs):
        if (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)) and Validator.is_type(text, str):
            super().__init__(master=parent, text=text)
            self.config(font=(var.LABEL_FONT, var.LABEL_FONT_SIZE), fg=var.LABEL_TEXTCOLOR)
            self.grid(kwargs)
        else:
            raise ValueError("Inappropriate arguments when creating a label!")


class Title(Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text, **kwargs)
        self.config(font=(var.TITLE_FONT, var.TITLE_FONT_SIZE), fg=var.TITLE_TEXTCOLOR)
