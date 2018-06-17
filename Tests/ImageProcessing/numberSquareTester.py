from unittest import TestCase
from ImageProcessing.numberSquare import NumberSquare
from Common.Errors import InappropriateArgsError, AddingPointError


class NumberSquareTester(TestCase):
    def test_incorrect_add_point(self):
        square = NumberSquare(3, 0)
        self.assertRaises(InappropriateArgsError, lambda: square.add_point(1, -1))
        self.assertRaises(InappropriateArgsError, lambda: square.add_point(1, "1"))
        self.assertRaises(InappropriateArgsError, lambda: square.add_point(-1, 1))
        self.assertRaises(InappropriateArgsError, lambda: square.add_point("1", 1))
        square.add_point(1, 1)
        square.add_point(2, 2)
        square.add_point(3, 3)
        square.add_point(4, 4)
        self.assertRaises(AddingPointError, lambda: square.add_point(1, 1))

    def test_get_points_and_correct_add_point(self):
        point1 = (1, 100)
        point2 = (400, 2)
        point3 = (23.2, 12)
        point4 = (982, 2133)
        square1 = NumberSquare(3, 0)
        square2 = NumberSquare(1, 1, point1)
        self.assertEqual(square1.get_points(), (None, None, None, None))
        self.assertEqual(square2.get_points(), (point1, None, None, None))
        square1.add_point(point1[0], point1[1])
        square2.add_point(point2[0], point2[1])
        self.assertEqual(square1.get_points(), (point1, None, None, None))
        self.assertEqual(square2.get_points(), (point1, point2, None, None))
        square1.add_point(point2[0], point2[1])
        square2.add_point(point3[0], point3[1])
        self.assertEqual(square1.get_points(), (point1, point2, None, None))
        self.assertEqual(square2.get_points(), (point1, point2, point3, None))
        square1.add_point(point3[0], point3[1])
        square2.add_point(point4[0], point4[1])
        self.assertEqual(square1.get_points(), (point1, point2, point3, None))
        self.assertEqual(square2.get_points(), (point1, point2, point3, point4))
        square1.add_point(point4[0], point4[1])
        self.assertEqual(square1.get_points(), (point1, point2, point3, point4))

    def test_incorrect_init(self):
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, -1))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, 1.1))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, "1"))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, 1, 1))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(10, 1))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, 10))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, 1, "Not tuple"))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, 1, [1, 1]))
        self.assertRaises(InappropriateArgsError, lambda: NumberSquare(1, 1, (1, -1)))

    def test_correct_init(self):
        square1 = NumberSquare(3, 0)
        point = (302, 101.2)
        square2 = NumberSquare(1, 1, point)
        self.assertEqual(square1.x_position, 3)
        self.assertEqual(square1.y_position, 0)
        self.assertEqual(square1.tl_point, None)
        self.assertEqual(square2.tl_point, point)
        self.assertEqual(square1.tr_point, None)
        self.assertEqual(square1.bl_point, None)
        self.assertEqual(square1.br_point, None)
