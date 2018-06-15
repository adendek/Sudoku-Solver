from unittest import TestCase
from Tests.GUI.Framework.widgetTester import test  # simple function
from Common.validationFunctions import Validator


class ValidatorTester(TestCase):
    def test_incorrect_is_function(self):
        self.assertEqual(Validator.is_function("Not a function"), False)
        self.assertEqual(Validator.is_function(3), False)
        self.assertEqual(Validator.is_function([test, "Nope", "not"]), False)

    def test_correct_is_function(self):
        self.assertEqual(Validator.is_function(test), True)
        self.assertEqual(Validator.is_function([test, test]), True)

    def test_incorrect_is_positive_number(self):
        self.assertEqual(Validator.is_positive_number(-1), False)
        self.assertEqual(Validator.is_positive_number(-1.0), False)
        self.assertEqual(Validator.is_positive_number("wrong"), False)
        self.assertEqual(Validator.is_positive_number([-1.0, -2, 3, "wrong"]), False)

    def test_correct_is_positive_number(self):
        self.assertEqual(Validator.is_positive_number(1), True)
        self.assertEqual(Validator.is_positive_number(1.0), True)
        self.assertEqual(Validator.is_positive_number(0.0), True)
        self.assertEqual(Validator.is_positive_number(-0.0), True)
        self.assertEqual(Validator.is_positive_number([1.0, 2, 3]), True)

    def test_correct_is_type(self):
        self.assertEqual(Validator.is_type(1, int), True)
        self.assertEqual(Validator.is_type("1", str), True)
        self.assertEqual(Validator.is_type(1.0, float), True)
        self.assertEqual(Validator.is_type([1, 2, 3], int), True)
        self.assertEqual(Validator.is_type(["1", "2", "3"], str), True)
        self.assertEqual(Validator.is_type([1.0, 2.1, 3.2], float), True)
        self.assertEqual(Validator.is_type([], int), True)

    def test_incorrect_is_type(self):
        self.assertEqual(Validator.is_type(1.0, int), False)
        self.assertEqual(Validator.is_type(1, str), False)
        self.assertEqual(Validator.is_type("1.0", float), False)
        self.assertEqual(Validator.is_type([1, "1", 3], int), False)
        self.assertEqual(Validator.is_type(["1", 2, "3"], str), False)
        self.assertEqual(Validator.is_type([1.0, 2.1, 3], float), False)

    def test_correct_is_number(self):
        self.assertEqual(Validator.is_number(1), True)
        self.assertEqual(Validator.is_number(1.0), True)
        self.assertEqual(Validator.is_number([1, 2.0, 3, 4.4]), True)

    def test_incorrect_is_number(self):
        self.assertEqual(Validator.is_number("1"), False)
        self.assertEqual(Validator.is_number([1, 2.0, "3", 4.4]), False)
