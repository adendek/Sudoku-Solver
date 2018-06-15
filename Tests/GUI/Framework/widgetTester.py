from unittest import TestCase
from GUI.Framework import widgets
from GUI.variables import variables
import tkinter
from tkinter import TclError


class WidgetTester(TestCase):
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



