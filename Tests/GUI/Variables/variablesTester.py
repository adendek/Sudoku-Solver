import GUI.Variables.variables as var
from unittest import TestCase


class VariablesTester(TestCase):
    def test_button(self):
        self.assertEqual(str, type(var.BUTTON_BACKGROUND))
        self.assertEqual(str, type(var.BUTTON_TEXTCOLOR))

    def test_label(self):
        self.assertEqual(str, type(var.LABEL_TEXTCOLOR))
        self.assertEqual(str, type(var.LABEL_FONT))
        self.assertEqual(int, type(var.LABEL_FONT_SIZE))
        self.assertGreater(var.LABEL_FONT_SIZE, 0)

    def test_title(self):
        self.assertEqual(str, type(var.TITLE_TEXTCOLOR))
        self.assertEqual(str, type(var.TITLE_FONT))
        self.assertEqual(int, type(var.TITLE_FONT_SIZE))
        self.assertGreater(var.TITLE_FONT_SIZE, 0)
        self.assertEqual(str, type(var.TITLE_TEXT))

    def test_border(self):
        self.assertEqual(int, type(var.BORDER))
        self.assertGreater(var.BORDER, 0)

    def test_sudoku_conf(self):
        self.assertEqual(int, type(var.SUDOKU_SQUARE_SIZE))
        self.assertGreater(var.SUDOKU_SQUARE_SIZE, 0)
        self.assertEqual(int, type(var.NUMBERS_SIZE))
        self.assertGreater(var.NUMBERS_SIZE, 0)
        self.assertEqual(str, type(var.NUMBERS_FONT))
        self.assertEqual(str, type(var.SQUARE_COLOR))
        self.assertEqual(str, type(var.SQUARE_ERR_COLOR))

    def test_path(self):
        self.assertEqual(str, type(var.ICON_PATH))
