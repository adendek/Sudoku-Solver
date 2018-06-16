from unittest import TestCase
from GUI.Framework.sudokuFieldTemplate import SudokuFieldTemplate
import GUI.Framework.widgets as widgets
from Tests.GUI.Framework.widgetTester import test  # simple test function
from GUI.capureImageView import CaptureImageView
from GUI.askIfCorrectView import AskIfCorrectView


class SudokuFieldTemplateTester(TestCase):
    def test_generate_field(self):
        field = [
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
        ]
        template = SudokuFieldTemplate("button1", test, field, AskIfCorrectView)
        self.assertEqual(len(template.text_edits), 81)  # 9x9

    def test_incorrect_init(self):
        wrong_field = [
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, -5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
        ]  # for other fields is already tested

        correct_field = [
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
        ]

        self.assertRaises(ValueError, lambda: SudokuFieldTemplate("button1", test, wrong_field, AskIfCorrectView))
        self.assertRaises(ValueError, lambda: SudokuFieldTemplate(1, test, correct_field, AskIfCorrectView))
        self.assertRaises(ValueError, lambda: SudokuFieldTemplate("button1", 1, correct_field, AskIfCorrectView))

        self.assertRaises(ValueError, lambda: SudokuFieldTemplate("button1", test, wrong_field, CaptureImageView))
        self.assertRaises(ValueError, lambda: SudokuFieldTemplate(1, test, correct_field, CaptureImageView))
        self.assertRaises(ValueError, lambda: SudokuFieldTemplate("button1", 1, correct_field, CaptureImageView))

    def test_correct_init(self):
        field = [
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
        ]
        template = SudokuFieldTemplate("button1", test, field, AskIfCorrectView)
        template2 = SudokuFieldTemplate("button1", test, field, CaptureImageView, readonly=True)
        self.assertEqual(type(template.content_frame), widgets.Frame)
        self.assertEqual(field, template.field_numbers)
        self.assertEqual(template.readonly, False)
        self.assertEqual(template2.readonly, True)
        self.assertEqual(type(template.text_edits), dict)
