import tkinter
import GUI.variables.variables as var
from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError


class TextEdit(tkinter.Entry):
    def __init__(self, parent, number, readonly=False, **kwargs):
        if Validator.is_positive_number(number) and Validator.is_type(number, int) and number <= 9 and\
                (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)) and \
                Validator.is_type(readonly, bool):
            self.value = tkinter.StringVar()
            self.value.trace('w', self._limit_size)
            super().__init__(master=parent, textvariable=self.value)
            self.grid(kwargs)
            self.config(justify='center', width=var.SUDOKU_SQUARE_SIZE, font=(var.NUMBERS_FONT, var.NUMBERS_SIZE))
            if number > 0:  # 0 is empty
                self.value.set(str(number))
            if readonly:
                self.config(state='readonly')
        else:
            raise InappropriateArgsError("creating an entry!")

    def get_value(self):
        return self.value.get()

    def _set_background(self):
        if self.config("background")[4] == var.SQUARE_ERR_COLOR:
            self.config({"background": var.SQUARE_COLOR})
        else:
            self.config({"background": var.SQUARE_ERR_COLOR})

    def _limit_size(self, *args):
        value = self.get_value()
        if len(value) > 0 and value[0] not in "123456789":  # it is not a number
            self.value.set("")
            self._set_background()  # set error color
            self.after(500, self._set_background)  # after 0.5s it will change color to white
        if len(value) > 1:
            self.value.set(value[:1])  # set to only first element
            self.config({"background": var.SQUARE_COLOR})


class Frame(tkinter.Frame):
    def __init__(self, parent, height=10, width=10, **kwargs):
        if Validator.is_positive_number([height, width]) and \
                (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)):
            super().__init__(master=parent, height=height, width=width)
            self.grid(kwargs)
        else:
            raise InappropriateArgsError("creating a frame!")


class Button(tkinter.Button):
    def __init__(self, parent, text, action, **kwargs):
        if (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)) \
                and Validator.is_type(text, str) and Validator.is_function(action):
            super().__init__(master=parent, text=text, command=action, width=12)
            self.config(bg=var.BUTTON_BACKGROUND, fg=var.BUTTON_TEXTCOLOR)
            self.grid(kwargs)
        else:
            raise InappropriateArgsError("creating a button!")


class Label(tkinter.Label):
    def __init__(self, parent, text, **kwargs):
        if (Validator.is_type(parent, tkinter.Tk) or Validator.is_type(parent, Frame)) and Validator.is_type(text, str):
            super().__init__(master=parent, text=text)
            self.config(font=(var.LABEL_FONT, var.LABEL_FONT_SIZE), fg=var.LABEL_TEXTCOLOR)
            self.grid(kwargs)
        else:
            raise InappropriateArgsError("creating a label!")


class Title(Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text, **kwargs)
        self.config(font=(var.TITLE_FONT, var.TITLE_FONT_SIZE), fg=var.TITLE_TEXTCOLOR)
