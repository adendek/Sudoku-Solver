from Common.Errors import InappropriateArgsError, SudokuFieldSizeError
from unittest import TestCase


class ErrorTester(TestCase):
    def test_sudoku_field_size_error(self):
        self.assertRaises(SudokuFieldSizeError, raise_sudoku_field_size_error)

    def test_inappropriate_args_error(self):
        self.assertRaises(InappropriateArgsError, raise_inappropriate_args_error, 1)
        self.assertRaises(InappropriateArgsError, raise_inappropriate_args_error, "1")
        self.assertRaises(InappropriateArgsError, raise_inappropriate_args_error, ["111"])


def raise_inappropriate_args_error(text):
    raise InappropriateArgsError(text)


def raise_sudoku_field_size_error():
    raise SudokuFieldSizeError()
