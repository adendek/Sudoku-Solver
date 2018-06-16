from unittest import TestCase
from GUI.Framework import widgets
from GUI.variables import variables
import tkinter
from tkinter import TclError


class WidgetTester(TestCase):
    def test_limit_size(self):
        root = tkinter.Tk()
        number = 1
        text_edit = widgets.TextEdit(root, number)
        text_edit.value.set("12")
        text_edit._limit_size()
        self.assertEqual(text_edit.get_value(), str(number))
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_COLOR)
        text_edit.value.set("a")
        self.assertEqual(text_edit.get_value(), "")
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_ERR_COLOR)

    def test_set_background(self):
        root = tkinter.Tk()
        text_edit = widgets.TextEdit(root, 1)
        text_edit._set_background()
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_ERR_COLOR)
        text_edit._set_background()
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_COLOR)

    def test_correct_get_value(self):
        root = tkinter.Tk()
        number = 3
        text_edit = widgets.TextEdit(root, number)
        self.assertEqual(text_edit.get_value(), str(number))

    def test_incorrect_text_edit(self):
        root = tkinter.Tk()
        self.assertRaises(ValueError, lambda: widgets.TextEdit(root, -1))
        self.assertRaises(ValueError, lambda: widgets.TextEdit(root, 1.1))
        self.assertRaises(ValueError, lambda: widgets.TextEdit(root, "1"))
        self.assertRaises(ValueError, lambda: widgets.TextEdit(root, 10))  # max number should be 9
        self.assertRaises(ValueError, lambda: widgets.TextEdit("not a root!", 1))
        self.assertRaises(TclError, lambda: widgets.TextEdit(root, 1, wrong="This does not exist!"))
        self.assertRaises(TclError, lambda: widgets.TextEdit(root, 1, row="Should be integer!"))
        self.assertRaises(ValueError, lambda: widgets.TextEdit("not a root!", 1, 3))
        self.assertRaises(ValueError, lambda: widgets.TextEdit("not a root!", 1, "1"))

    def test_correct_text_edit(self):
        root = tkinter.Tk()
        input_number = 0
        input_number2 = 1
        entry = widgets.TextEdit(root, input_number)
        entry2 = widgets.TextEdit(root, input_number2, readonly=True)
        self.assertNotEqual(entry.get(), str(input_number))  # it shouldn't be set if number is 0
        self.assertEqual(entry2.get(), str(input_number2))
        self.assertEqual(entry.cget("justify"), "center")
        self.assertEqual(entry2.value.get(), str(input_number2))
        self.assertEqual(type(entry.value), tkinter.StringVar)
        self.assertEqual(entry.cget("width"), variables.SUDOKU_SQUARE_SIZE)
        self.assertEqual(entry.cget("font"), variables.NUMBERS_FONT + " " + str(variables.NUMBERS_SIZE))
        self.assertEqual(entry.cget("state"), "normal")
        self.assertEqual(entry2.cget("state"), "readonly")

    def test_incorrect_frame(self):
        root = tkinter.Tk()
        self.assertRaises(ValueError, lambda: widgets.Frame("Not cool", 1, 1))
        self.assertRaises(ValueError, lambda: widgets.Frame(root, -2, -1))
        self.assertRaises(TclError, lambda: widgets.Frame(root, 1, 1, wrong="This does not exist!"))
        self.assertRaises(TclError, lambda: widgets.Frame(root, 1, 1, row="Should be integer!"))

    def test_correct_frame(self):
        root = tkinter.Tk()
        width, height = 200, 200
        frame = widgets.Frame(root, width, height)
        self.assertEqual(frame.cget("width"), width)
        self.assertEqual(frame.cget("height"), height)

    def test_incorrect_title(self):
        root = tkinter.Tk()
        text = "Correct"
        self.assertRaises(ValueError, lambda: widgets.Title("Not cool", text))
        self.assertRaises(ValueError, lambda: widgets.Title(root, 1))
        self.assertRaises(TclError, lambda: widgets.Title(root, text, wrong="This does not exist!"))
        self.assertRaises(TclError, lambda: widgets.Title(root, text, row="Should be integer!"))

    def test_correct_title(self):
        root = tkinter.Tk()
        text = "Correct"
        title = widgets.Title(root, text)
        self.assertEqual(title.cget("text"), text)
        self.assertEqual(title.cget("fg"), variables.TITLE_TEXTCOLOR)
        self.assertEqual(title.cget("font"), variables.TITLE_FONT + " " + str(variables.TITLE_FONT_SIZE))

    def test_incorrect_label(self):
        root = tkinter.Tk()
        text = "Correct"
        self.assertRaises(ValueError, lambda: widgets.Label("Not cool", text))
        self.assertRaises(ValueError, lambda: widgets.Label(root, 1))
        self.assertRaises(TclError, lambda: widgets.Label(root, text, wrong="This does not exist!"))
        self.assertRaises(TclError, lambda: widgets.Label(root, text, row="Should be integer!"))

    def test_correct_label(self):
        root = tkinter.Tk()
        text = "Correct"
        label = widgets.Label(root, text)
        self.assertEqual(label.cget("text"), text)
        self.assertEqual(label.cget("fg"), variables.LABEL_TEXTCOLOR)
        self.assertEqual(label.cget("font"), variables.LABEL_FONT + " " + str(variables.LABEL_FONT_SIZE))

    def test_incorrect_button(self):
        root = tkinter.Tk()
        text = "Correct"
        self.assertRaises(ValueError, lambda: widgets.Button("Not cool", text, test))
        self.assertRaises(ValueError, lambda: widgets.Button(root, 1, test))
        self.assertRaises(ValueError, lambda: widgets.Button(root, text, text))
        self.assertRaises(TclError, lambda: widgets.Button(root, text, test, wrong="This does not exist!"))
        self.assertRaises(TclError, lambda: widgets.Button(root, text, test, row="Should be integer!"))

    def test_correct_button(self):
        root = tkinter.Tk()
        text = "Correct"
        button = widgets.Button(root, text, test)
        self.assertEqual(button.cget("text"), text)
        self.assertEqual(button.cget("bg"), variables.BUTTON_BACKGROUND)
        self.assertEqual(button.cget("fg"), variables.BUTTON_TEXTCOLOR)


def test():
    return True
