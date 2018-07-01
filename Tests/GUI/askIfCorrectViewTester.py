from GUI.askIfCorrectView import AskIfCorrectView
from Common.Errors import InappropriateArgsError
from GUI.Framework.widgets import Button
from unittest import TestCase
import tkinter


class AskIfCorrectViewTester(TestCase):
    def setUp(self):
        self.field = [
            [6, 5, 0, 8, 7, 3, 0, 9, 0],
            [0, 0, 3, 2, 5, 0, 0, 0, 8],
            [9, 8, 0, 1, 0, 4, 3, 5, 7],
            [1, 0, 5, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, 5, 0, 3],
            [5, 7, 8, 3, 0, 1, 0, 2, 6],
            [2, 0, 0, 0, 4, 8, 9, 0, 0],
            [0, 9, 0, 6, 2, 5, 0, 8, 1]
        ]
        self.incorrect_field = [
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
            [1, 0, 2, 0, 0, 0, 5, 3, 4],
        ]
        self.unsolvable_field = [
            [1, 2, 0, 4, 5, 6, 7, 8, 9],
            [0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.wrong_field = [
            [1, 2, 0, 4, 5, 6, 7, 8, 9],
            [0, 0, 3, 0, 0, 0, 0, 0, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.view = AskIfCorrectView(self.field, tkinter.Tk)
        self.view2 = AskIfCorrectView(self.unsolvable_field, tkinter.Tk)
        self.view3 = AskIfCorrectView(self.wrong_field, tkinter.Tk)

    def test_get_current_field(self):
        expected_output = [
            [6, 5, 1, 8, 7, 3, 2, 9, 4],
            [7, 4, 3, 2, 5, 9, 1, 6, 8],
            [9, 8, 2, 1, 6, 4, 3, 5, 7],
            [1, 2, 5, 4, 3, 6, 8, 7, 9],
            [4, 3, 9, 5, 8, 7, 6, 1, 2],
            [8, 6, 7, 9, 1, 2, 5, 4, 3],
            [5, 7, 8, 3, 9, 1, 4, 2, 6],
            [2, 1, 6, 7, 4, 8, 9, 3, 5],
            [3, 9, 4, 6, 2, 5, 7, 8, 1]
        ]
        correct_detected = [0, 1, 3, 4, 5, 7, 11, 12, 13, 17, 18, 19, 21, 23, 24, 25, 26, 27, 29, 36, 44, 49, 51, 53,
                            54, 55, 56, 57, 59, 61, 62, 63, 67, 68, 69, 73, 75, 76, 77, 79, 80]
        solution, detected = self.view._get_current_field()
        self.assertEqual(solution, expected_output)
        self.assertEqual(correct_detected, detected)
        solution2, detected2 = self.view2._get_current_field()
        self.assertEqual(solution2, False)
        self.assertEqual(list, type(detected2))
        solution3, detected3 = self.view3._get_current_field()
        self.assertEqual(solution3, False)
        self.assertEqual(list, type(detected3))

    def test_incorrect_init(self):
        self.assertRaises(InappropriateArgsError, AskIfCorrectView, self.incorrect_field, tkinter.Tk)

    def test_correct_init(self):
        self.assertEqual(self.view.info_label["text"], self.view.label_text)
        self.assertEqual(type(self.view.show_image_button), Button)
