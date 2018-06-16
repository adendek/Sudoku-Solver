from Tests.GUI.Framework.widgetTester import test  # simple function
from GUI.Framework.mainTemplate import MainTemplate
import GUI.Framework.widgets as widgets
import GUI.variables.variables as var
from unittest import TestCase


class MainTemplateTester(TestCase):
    def test_set_to_screen_center(self):
        template = MainTemplate("first", test, "second", test)
        before = template.geometry()
        template._set_to_screen_center()
        after = template.geometry()
        self.assertNotEqual(before, after)  # chances that they are going to be the same are very low

    def test_incorrect_calculate_middle(self):
        template = MainTemplate("first", test, "second", test)
        self.assertRaises(ValueError, lambda: template._calculate_middle("1", 20))
        self.assertRaises(ValueError, lambda: template._calculate_middle(1, "20"))
        self.assertRaises(ValueError, lambda: template._calculate_middle(-1, -0))

    def test_correct_calculate_middle(self):
        template = MainTemplate("first", test, "second", test)
        width = template.winfo_width()
        height = template.winfo_height()
        result = (template.winfo_screenwidth() // 2) - (width // 2), (template.winfo_screenheight() // 2) - (height // 2)
        self.assertEqual(template._calculate_middle(width, height), result)

    def test_get_window_size(self):
        template = MainTemplate("first", test, "second", test)
        self.assertEqual(template._get_window_size(), (template.winfo_width(), template.winfo_height()))

    def test_incorrect_init(self):
        self.assertRaises(ValueError, lambda: MainTemplate(1, test, "ok", test))
        self.assertRaises(ValueError, lambda: MainTemplate("ok", test, 1, test))
        self.assertRaises(ValueError, lambda: MainTemplate("ok", test, ["almost", "or is it?"], test))
        self.assertRaises(ValueError, lambda: MainTemplate("ok", "hmm", "ok", test))
        self.assertRaises(ValueError, lambda: MainTemplate("ok", test, "ok", "hmm"))
        self.assertRaises(ValueError, lambda: MainTemplate("ok", test, "ok", 3))

    def test_correct_init(self):
        first_button_text = "first button"
        second_button_text = "second button"
        template = MainTemplate(first_button_text, test, second_button_text, test)
        self.assertEqual(type(template.left_button_frame), widgets.Frame)
        self.assertEqual(type(template.right_button_frame), widgets.Frame)
        self.assertEqual(type(template.bot_frame), widgets.Frame)
        self.assertEqual(type(template.title_frame), widgets.Frame)
        self.assertEqual(type(template.info_frame), widgets.Frame)
        self.assertEqual(type(template.left_button), widgets.Button)
        self.assertEqual(type(template.right_button), widgets.Button)
        self.assertEqual(type(template.title_label), widgets.Title)
        self.assertEqual(type(template.info_label), widgets.Label)
        self.assertEqual(template.protocol("WM_DELETE_WINDOW")[-11:], "_on_destroy")  # name of the function
        self.assertEqual(template.left_button.config("command")[4][-4:], "test")  # if function is set (to test)
        self.assertEqual(template.right_button.config("command")[4][-4:], "test")  # if function is set (to test)
        self.assertEqual(template.right_button.config("text")[4], second_button_text)  # if function is set (to test)
        self.assertEqual(template.left_button.config("text")[4], first_button_text)  # if function is set (to test)
        self.assertEqual(template.title(), var.TITLE_TEXT)
        self.assertEqual(template.bot_frame.grid_columnconfigure(0)["weight"], 1)
        self.assertEqual(template.bot_frame.grid_columnconfigure(1)["weight"], 1)
        self.assertEqual(template.resizable(), (False, False))  # false in x and y direction
