from Common.Errors import InappropriateArgsError
from GUI.Variables import variables
from GUI.Framework import widgets
from unittest import TestCase
from tkinter import TclError
import tkinter


class WidgetTester(TestCase):
    def setUp(self):
        self.root = tkinter.Tk()
        
    def test_limit_size(self):
        number = 1
        text_edit = widgets.TextEdit(self.root, number)
        text_edit.value.set("12")
        text_edit._limit_size()
        self.assertEqual(text_edit.get_value(), str(number))
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_COLOR)
        text_edit.value.set("a")
        self.assertEqual(text_edit.get_value(), "")
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_ERR_COLOR)
 
    def test_set_background(self):   
        text_edit = widgets.TextEdit(self.root, 1)
        text_edit._set_background()
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_ERR_COLOR)
        text_edit._set_background()
        self.assertEqual(text_edit.config("background")[4], variables.SQUARE_COLOR)

    def test_correct_get_value(self):
        number = 3
        text_edit = widgets.TextEdit(self.root, number)
        self.assertEqual(text_edit.get_value(), str(number))

    def test_incorrect_text_edit(self):
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, self.root, -1)
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, self.root, 1.1)
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, self.root, "1")
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, self.root, 10)  # max number should be 9
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, "not a self.root!", 1)
        self.assertRaises(TclError, widgets.TextEdit, self.root, 1, wrong="This does not exist!")
        self.assertRaises(TclError, widgets.TextEdit, self.root, 1, row="Should be integer!")
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, "not a self.root!", 1, 3)
        self.assertRaises(InappropriateArgsError, widgets.TextEdit, "not a self.root!", 1, "1")

    def test_correct_text_edit(self):  
        input_number = 0
        input_number2 = 1
        entry = widgets.TextEdit(self.root, input_number)
        entry2 = widgets.TextEdit(self.root, input_number2, readonly=True)
        self.assertNotEqual(entry.get_value(), str(input_number))  # it shouldn't be set if number is 0
        self.assertEqual(entry2.get_value(), str(input_number2))
        self.assertEqual(entry.cget("justify"), "center")
        self.assertEqual(type(entry.value), tkinter.StringVar)
        self.assertEqual(entry.cget("width"), variables.SUDOKU_SQUARE_SIZE)
        self.assertEqual(entry.cget("font"), variables.NUMBERS_FONT + " " + str(variables.NUMBERS_SIZE))
        self.assertEqual(entry.cget("state"), "normal")
        self.assertEqual(entry2.cget("state"), "readonly")

    def test_incorrect_frame(self):
        self.assertRaises(InappropriateArgsError, widgets.Frame, "Not cool", 1, 1)
        self.assertRaises(InappropriateArgsError, widgets.Frame, self.root, -2, -1)
        self.assertRaises(TclError, widgets.Frame, self.root, 1, 1, wrong="This does not exist!")
        self.assertRaises(TclError, widgets.Frame, self.root, 1, 1, row="Should be integer!")

    def test_correct_frame(self):   
        width, height = 200, 200
        frame = widgets.Frame(self.root, width, height)
        self.assertEqual(frame.cget("width"), width)
        self.assertEqual(frame.cget("height"), height)

    def test_incorrect_title(self):   
        text = "Correct"
        self.assertRaises(InappropriateArgsError, widgets.Title, "Not cool", text)
        self.assertRaises(InappropriateArgsError, widgets.Title, self.root, 1)
        self.assertRaises(TclError, widgets.Title, self.root, text, wrong="This does not exist!")
        self.assertRaises(TclError, widgets.Title, self.root, text, row="Should be integer!")

    def test_correct_title(self):
        text = "Correct"
        title = widgets.Title(self.root, text)
        self.assertEqual(title.cget("text"), text)
        self.assertEqual(title.cget("fg"), variables.TITLE_TEXTCOLOR)
        self.assertEqual(title.cget("font"), variables.TITLE_FONT + " " + str(variables.TITLE_FONT_SIZE))

    def test_incorrect_label(self):  
        text = "Correct"
        self.assertRaises(InappropriateArgsError, widgets.Label, "Not cool", text)
        self.assertRaises(InappropriateArgsError, widgets.Label, self.root, 1)
        self.assertRaises(TclError, widgets.Label, self.root, text, wrong="This does not exist!")
        self.assertRaises(TclError, widgets.Label, self.root, text, row="Should be integer!")

    def test_correct_label(self):
        text = "Correct"
        label = widgets.Label(self.root, text)
        self.assertEqual(label.cget("text"), text)
        self.assertEqual(label.cget("fg"), variables.LABEL_TEXTCOLOR)
        self.assertEqual(label.cget("font"), variables.LABEL_FONT + " " + str(variables.LABEL_FONT_SIZE))

    def test_incorrect_button(self):  
        text = "Correct"
        self.assertRaises(InappropriateArgsError, widgets.Button, "Not cool", text, test)
        self.assertRaises(InappropriateArgsError, widgets.Button, self.root, 1, test)
        self.assertRaises(InappropriateArgsError, widgets.Button, self.root, text, text)
        self.assertRaises(TclError, widgets.Button, self.root, text, test, wrong="This does not exist!")
        self.assertRaises(TclError, widgets.Button, self.root, text, test, row="Should be integer!")

    def test_correct_button(self): 
        text = "Correct"
        button = widgets.Button(self.root, text, test)
        self.assertEqual(button.cget("text"), text)
        self.assertEqual(button.cget("bg"), variables.BUTTON_BACKGROUND)
        self.assertEqual(button.cget("fg"), variables.BUTTON_TEXTCOLOR)


def test():
    return True
