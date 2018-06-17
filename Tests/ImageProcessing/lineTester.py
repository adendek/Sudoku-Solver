from unittest import TestCase
from ImageProcessing.line import Line, Orientation
from Common.Errors import InappropriateArgsError


class LineTester(TestCase):
    def test_incorrect_get_intersection(self):
        line = Line(0, 1, 2, 3)
        self.assertRaises(InappropriateArgsError, lambda: Line.get_intersection(1, line))
        self.assertRaises(InappropriateArgsError, lambda: Line.get_intersection(line, 1))
        self.assertRaises(InappropriateArgsError, lambda: Line.get_intersection("1", line))
        self.assertRaises(InappropriateArgsError, lambda: Line.get_intersection(dict, line))

    def test_correct_get_intersection(self):
        line1 = Line(2, 5, 3, 0)
        line2 = Line(1, 3, 0, 0)
        line3 = Line(4.34, 3.96, 4.14, 2.28)
        line4 = Line(3, 0, 4, 3)
        self.assertEqual(Line.get_intersection(line1, line2), (round(1.88), round(5.63)))
        self.assertEqual(Line.get_intersection(line1, line3), (round(3.54), round(-2.72)))
        self.assertEqual(Line.get_intersection(line2, line4), False)

    def test_incorrect_coefs(self):
        self.assertRaises(InappropriateArgsError, lambda: Line.get_coefs("Not a line"))
        self.assertRaises(InappropriateArgsError, lambda: Line.get_coefs(3))
        self.assertRaises(InappropriateArgsError, lambda: Line.get_coefs(dict))

    def test_correct_coefs(self):
        line1 = Line(3, 2, 1, 0)
        line2 = Line(30, 2, 2, 1)
        self.assertEqual(Line.get_coefs(line1), (2, -2, 2))
        self.assertEqual(Line.get_coefs(line2), (1, -28, -26))

    def test_configure_slope(self):
        line = Line(0, 0, 1, 0)
        line1 = Line(1, 0, 1, 1)
        line2 = Line(3, 2, 1, 0)
        line3 = Line(30, 2, 2, 1)
        self.assertEqual(line._configure_slope(), 0)
        self.assertEqual(line1._configure_slope(), 100)
        self.assertEqual(line2._configure_slope(), 1)
        self.assertEqual(line3._configure_slope(), 0.04)

    def test_get_orientation(self):
        line = Line(0, 0, 1, 0)
        self.assertEqual(line.orientation, line.get_orientation())

    def test_get_slope(self):
        line = Line(0, 0, 1, 0)
        self.assertEqual(line.slope, line.get_slope())

    def test_configure_orientation(self):
        self.assertEqual(Line(0, 0, 1, 0).orientation, Orientation.Horizontal)
        self.assertEqual(Line(0, 0, 1, 0.9).orientation, Orientation.Horizontal)
        self.assertEqual(Line(0, 0, 0, 1).orientation, Orientation.Vertical)
        self.assertEqual(Line(0, 0, 0.9, 1).orientation, Orientation.Vertical)

    def test_incorrect_init(self):
        self.assertRaises(InappropriateArgsError, lambda: Line(0, 0, 0, 0))  # point not a line
        self.assertRaises(InappropriateArgsError, lambda: Line(0, 0, 0, "1"))

    def test_correct_init(self):
        x1, y1, x2, y2 = 0, 0.0, 1.5, 0
        line = Line(x1, y1, x2, y2)
        self.assertEqual(line.x1, x1)
        self.assertEqual(line.y1, y1)
        self.assertEqual(line.x2, x2)
        self.assertEqual(line.y2, y2)
        self.assertEqual(line.orientation, Orientation.Horizontal)
        self.assertEqual(line.slope, line._configure_slope())
        x1, y1, x2, y2 = 0, 0.0, 0, 2.2
        line = Line(x1, y1, x2, y2)
        self.assertEqual(line.orientation, Orientation.Vertical)
        self.assertEqual(line.slope, line._configure_slope())
