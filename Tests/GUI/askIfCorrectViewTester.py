from GUI.askIfCorrectView import AskIfCorrectView
from unittest import TestCase
import tkinter
from Common.Errors import InappropriateArgsError


class AskIfCorrectViewTester(TestCase):
    def test_get_current_field(self):
        correct_field = [
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
        unsolvable_field = [
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
        wrong_field = [
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
        view1 = AskIfCorrectView(correct_field, tkinter.Tk)
        view2 = AskIfCorrectView(unsolvable_field, tkinter.Tk)
        view3 = AskIfCorrectView(wrong_field, tkinter.Tk)
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
        self.assertEqual(view1._get_current_field(), expected_output)
        self.assertEqual(view2._get_current_field(), False)
        self.assertEqual(view3._get_current_field(), False)

    def test_incorrect_init(self):
        field = [
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
        self.assertRaises(InappropriateArgsError, lambda: AskIfCorrectView(field, tkinter.Tk))

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
        view = AskIfCorrectView(field, tkinter.Tk)
        self.assertNotEqual(view.info_label["text"], "")
