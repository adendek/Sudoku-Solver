from Tests.GUI.Framework.widgetTester import test  # simple function
from GUI.Framework.mainTemplate import MainTemplate
from Common.Errors import InappropriateArgsError
import GUI.Framework.widgets as widgets
import GUI.Variables.variables as var
from unittest import TestCase


class MainTemplateTester(TestCase):
    def setUp(self):
        self.template = MainTemplate("first", test, "second", test)
    
    def test_incorrect_display_message(self):
        self.assertRaises(InappropriateArgsError, self.template.display_message, 1, "1", "black", 1)
        self.assertRaises(InappropriateArgsError, self.template.display_message, "1", 1, "black", 1)
        self.assertRaises(InappropriateArgsError, self.template.display_message, "1", "1", 1, 1)
        self.assertRaises(InappropriateArgsError, self.template.display_message, "1", "1", "black", "1")

    def test_display_message(self):
        before = self.template.info_label["text"]
        self.template.display_message("32435664532sdadc?-", "a", "green", 1)
        self.assertNotEqual(before, self.template.info_label["text"])
        self.assertEqual(self.template.info_label["fg"], "green")
        self.assertEqual("32435664532sdadc?-", self.template.info_label["text"])

    def test_incorrect_set_info_label(self):
        self.assertRaises(InappropriateArgsError, self.template.set_info_label, 1)
        self.assertRaises(InappropriateArgsError, self.template.set_info_label, ["not", "I", "hope"])
        self.assertRaises(InappropriateArgsError, self.template.set_info_label, -1.2)

    def test_correct_set_info_label(self):
        before = self.template.info_label["text"]
        self.template.set_info_label("32435664532sdadc?-")
        self.assertEqual(self.template.info_label["fg"], "black")
        self.assertNotEqual(before, self.template.info_label["text"])
        self.assertEqual("32435664532sdadc?-", self.template.info_label["text"])

    def test_set_to_screen_center(self):
        before = self.template.geometry()
        self.template._set_to_screen_center()
        after = self.template.geometry()
        self.assertNotEqual(before, after)  # chances that they are going to be the same are very low

    def test_incorrect_calculate_middle(self):
        self.assertRaises(InappropriateArgsError, self.template._calculate_middle, "1", 20)
        self.assertRaises(InappropriateArgsError, self.template._calculate_middle, 1, "20")
        self.assertRaises(InappropriateArgsError, self.template._calculate_middle, -1, -0)

    def test_correct_calculate_middle(self):
        width = self.template.winfo_width()
        height = self.template.winfo_height()
        result = (self.template.winfo_screenwidth() // 2) - (width // 2), (self.template.winfo_screenheight() // 2) - (height // 2)
        self.assertEqual(self.template._calculate_middle(width, height), result)

    def test_get_window_size(self):
        self.assertEqual(self.template._get_window_size(), (self.template.winfo_width(), self.template.winfo_height()))

    def test_incorrect_init(self):
        self.assertRaises(InappropriateArgsError, MainTemplate, 1, test, "ok", test)
        self.assertRaises(InappropriateArgsError, MainTemplate, "ok", test, 1, test)
        self.assertRaises(InappropriateArgsError, MainTemplate, "ok", test, ["almost", "or is it?"], test)
        self.assertRaises(InappropriateArgsError, MainTemplate, "ok", "hmm", "ok", test)
        self.assertRaises(InappropriateArgsError, MainTemplate, "ok", test, "ok", "hmm")
        self.assertRaises(InappropriateArgsError, MainTemplate, "ok", test, "ok", 3)

    def test_correct_init(self):
        first_button_text = "first button"
        second_button_text = "second button"
        self.template = MainTemplate(first_button_text, test, second_button_text, test)
        self.assertEqual(type(self.template.left_button_frame), widgets.Frame)
        self.assertEqual(type(self.template.right_button_frame), widgets.Frame)
        self.assertEqual(type(self.template.bot_frame), widgets.Frame)
        self.assertEqual(type(self.template.title_frame), widgets.Frame)
        self.assertEqual(type(self.template.info_frame), widgets.Frame)
        self.assertEqual(type(self.template.left_button), widgets.Button)
        self.assertEqual(type(self.template.right_button), widgets.Button)
        self.assertEqual(type(self.template.title_label), widgets.Title)
        self.assertEqual(type(self.template.info_label), widgets.Label)
        self.assertEqual(self.template.protocol("WM_DELETE_WINDOW")[-11:], "_on_destroy")  # name of the function
        self.assertEqual(self.template.left_button.config("command")[4][-4:], "test")  # if function is set (to test)
        self.assertEqual(self.template.right_button.config("command")[4][-4:], "test")  # if function is set (to test)
        self.assertEqual(self.template.right_button.config("text")[4], second_button_text)  # if function is set (to test)
        self.assertEqual(self.template.left_button.config("text")[4], first_button_text)  # if function is set (to test)
        self.assertEqual(self.template.title(), var.TITLE_TEXT)
        self.assertEqual(self.template.bot_frame.grid_columnconfigure(0)["weight"], 1)
        self.assertEqual(self.template.bot_frame.grid_columnconfigure(2)["weight"], 1)
        self.assertEqual(self.template.resizable(), (False, False))  # false in x and y direction
