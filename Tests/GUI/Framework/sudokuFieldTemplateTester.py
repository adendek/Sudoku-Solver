from GUI.Framework.sudokuFieldTemplate import SudokuFieldTemplate
from Tests.GUI.Framework.widgetTester import test  # simple test function
from GUI.askIfCorrectView import AskIfCorrectView
from GUI.capureImageView import CaptureImageView
from Common.Errors import InappropriateArgsError
import GUI.Framework.widgets as widgets
from unittest import TestCase


class SudokuFieldTemplateTester(TestCase):
    def setUp(self):
        self.field = [
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
        self.template = SudokuFieldTemplate("button1", test, self.field, AskIfCorrectView)
        self.template2 = SudokuFieldTemplate("button1", test, self.field, CaptureImageView, readonly=True, detected=[0, 1])
        
    def test_generate_field(self):
        self.assertEqual(len(self.template.text_edits), 9)  # 9x9
        self.assertEqual(len(self.template.text_edits[0]), 9)
        self.assertEqual(len(self.template.text_edits[1]), 9)
        self.assertEqual(len(self.template.text_edits[2]), 9)
        self.assertEqual(len(self.template.text_edits[3]), 9)
        self.assertEqual(len(self.template.text_edits[4]), 9)
        self.assertEqual(len(self.template.text_edits[5]), 9)
        self.assertEqual(len(self.template.text_edits[6]), 9)
        self.assertEqual(len(self.template.text_edits[7]), 9)
        self.assertEqual(len(self.template.text_edits[8]), 9)

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

        self.assertRaises(InappropriateArgsError, SudokuFieldTemplate, "button1", test, wrong_field, AskIfCorrectView)
        self.assertRaises(InappropriateArgsError, SudokuFieldTemplate, 1, test, correct_field, AskIfCorrectView)
        self.assertRaises(InappropriateArgsError, SudokuFieldTemplate, "button1", 1, correct_field, AskIfCorrectView)
        self.assertRaises(InappropriateArgsError, SudokuFieldTemplate, "button1", test, wrong_field, CaptureImageView)
        self.assertRaises(InappropriateArgsError, SudokuFieldTemplate, 1, test, correct_field, CaptureImageView)
        self.assertRaises(InappropriateArgsError, SudokuFieldTemplate, "button1", 1, correct_field, CaptureImageView)

    def test_correct_init(self):
        self.assertEqual(type(self.template.content_frame), widgets.Frame)
        self.assertEqual(self.field, self.template.field_numbers)
        self.assertEqual(self.template.readonly, False)
        self.assertEqual(self.template2.readonly, True)
        self.assertEqual(type(self.template.text_edits), list)
        self.assertEqual(type(self.template.text_edits[0]), list)
        self.assertEqual(type(self.template.text_edits[1]), list)
        self.assertEqual(type(self.template.text_edits[2]), list)
        self.assertEqual(type(self.template.text_edits[3]), list)
        self.assertEqual(type(self.template.text_edits[4]), list)
        self.assertEqual(type(self.template.text_edits[5]), list)
        self.assertEqual(type(self.template.text_edits[6]), list)
        self.assertEqual(type(self.template.text_edits[7]), list)
        self.assertEqual(type(self.template.text_edits[8]), list)
        self.assertEqual(self.template.detected, [])
        self.assertEqual(self.template2.detected, [0, 1])
