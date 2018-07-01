from Common.Errors import InappropriateArgsError, SudokuFieldSizeError
from ImageProcessing.extractSudokuField import ExtractField
from Common.validationFunctions import Validator
from unittest import TestCase
import numpy as np
import cv2
import os

PATH = os.path.dirname(os.path.realpath(__file__))


class ExtractSudokuFieldTester(TestCase):
    def setUp(self):
        self.path = PATH + "/../../SamplePictures/sudoku.jpg"
        self.field = ExtractField(self.path)
        
    def test_incorrect_hide_smaller_blobs(self):
        self.assertRaises(InappropriateArgsError, self.field._hide_smaller_blobs, 1)
        self.assertRaises(InappropriateArgsError, self.field._hide_smaller_blobs, "1")

    def test_incorrect_hough_lines(self):
        self.assertRaises(InappropriateArgsError, self.field._get_hough_lines, 1)
        self.assertRaises(InappropriateArgsError, self.field._get_hough_lines, "1")

    def test_get_hough_lines(self):
        result = self.field._get_hough_lines(self.field.changing_img)
        self.assertEqual(type(result), np.ndarray)

    def test_incorrect_get_longest_line(self):
        ok = (1, 1)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, 1, ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, "1", ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, ok, 1, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, ok, "1", ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, ok, ok, 1, ok)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, ok, ok, "1", ok)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, ok, ok, ok, 1)
        self.assertRaises(InappropriateArgsError, self.field._get_longest_line, ok, ok, ok, "1")

    def test_correct_get_longest_line(self):
        tl, tr, bl, br = (0, 0), (100, 0), (0, 100), (100, 100)
        self.assertEqual(type(self.field._get_longest_line(tl, tr, bl, br)), float)
        self.assertEqual(self.field._get_longest_line(tl, tr, bl, br), 100)
        tl, tr, bl, br = (0, 0), (100, 0), (0, 100), (100, 50)  # the difference is to big
        self.assertRaises(SudokuFieldSizeError, self.field._get_longest_line, tl, tr, bl, br)

    def test_incorrect_draw_point(self):
        ok_point = (1, 1)
        ok_img = self.field.img
        self.assertRaises(InappropriateArgsError, self.field.draw_point, "false", ok_point)
        self.assertRaises(InappropriateArgsError, self.field.draw_point, ok_img, "1")

    def test_incorrect_distance_between_points(self):
        self.assertRaises(InappropriateArgsError, self.field._get_distance_between_points, 1, (3, -4))
        self.assertRaises(InappropriateArgsError, self.field._get_distance_between_points, (1, 1), 3)
        self.assertRaises(InappropriateArgsError, self.field._get_distance_between_points, "1", (3, -4))
        self.assertRaises(InappropriateArgsError, self.field._get_distance_between_points, (1, 1), "1")

    def get_correct_distance_between_points(self):
        result = self.field._get_distance_between_points((-1, 3), (3, -4))
        self.assertEqual(type(result), float)
        self.assertGreater(result, 0)
        self.assertEqual(result, 8.026)

    def test_init_points(self):
        result = self.field._init_points()
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 4)
        correct_result = ((self.field.width, self.field.height), (0, self.field.height), (self.field.width, 0), (0, 0))
        self.assertEqual(result, correct_result)

    def test_incorrect_update_corners(self):
        ok = (1, 1)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, "1", 1, ok, ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, -1, 1, ok, ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, 1, "1", ok, ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, -1, 1, ok, ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, -1, 1, 1, ok, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, -1, 1, ok, 1, ok, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, -1, 1, ok, ok, 1, ok)
        self.assertRaises(InappropriateArgsError, self.field._update_corners, -1, 1, ok, ok, ok, 1)

    def test_correct_update_corners(self):
        tl, tr, bl, bt = (100, 100), (100, 100), (100, 100), (100, 100)
        result = self.field._update_corners(1, 1, tl, tr, bl, bt)
        self.assertEqual(result, (tl, tr, bl, bt))  # shouldn't change anything
        result = self.field._update_corners(74, 84, tl, tr, bl, bt)
        self.assertNotEqual(result, (tl, tr, bl, bt))

    def test_corner_points(self):
        result = self.field._get_corner_points()
        self.assertEqual(len(result), 4)
        self.assertEqual(type(result), tuple)
        self.assertEqual(Validator.is_positive_number(list(result[0])), True)
        self.assertEqual(Validator.is_positive_number(list(result[1])), True)
        self.assertEqual(Validator.is_positive_number(list(result[2])), True)
        self.assertEqual(Validator.is_positive_number(list(result[3])), True)
        self.assertEqual(result, ((74, 84), (492, 70), (37, 512), (520, 520)))

    def test_incorrect_get_points_on_line(self):
        self.assertRaises(InappropriateArgsError, self.field._get_points_on_line, 1, "1")
        self.assertRaises(InappropriateArgsError, self.field._get_points_on_line, "1", 1)

    def test_correct_get_points_on_line(self):
        result = self.field._get_points_on_line(3, 3)
        self.assertEqual(type(result), tuple)
        self.assertEqual(Validator.is_number(list(result)), True)
        self.assertEqual(result, (-144, -989, 138, 990))

    def test_incorrect_get_intersection_points(self):
        lines = self.field._seperate_lines(self.field._get_hough_lines(self.field.changing_img))
        line = lines[0]
        self.assertRaises(InappropriateArgsError, self.field._get_intersection_point, line, 1)
        self.assertRaises(InappropriateArgsError, self.field._get_intersection_point, line, "1")
        self.assertRaises(InappropriateArgsError, self.field._get_intersection_point, 1, line)
        self.assertRaises(InappropriateArgsError, self.field._get_intersection_point, "1", line)

    def test_correct_get_intersection_points(self):
        lines = self.field._seperate_lines(self.field._get_hough_lines(self.field.changing_img))
        line1 = lines[0][0]
        line2 = lines[1][0]
        result = self.field._get_intersection_point(line1, line2)
        self.assertEqual(type(result), tuple)
        self.assertEqual(type(result[0]), int)
        self.assertEqual(type(result[1]), int)
        self.assertEqual(result, (520, 520))

    def test_correct_get_criteria_flags_attempts(self):
        criteria, flags, attempts = self.field._get_criteria_flags_attempts()
        self.assertEqual(type(criteria), tuple)
        self.assertEqual(len(criteria), 3)
        self.assertEqual(type(flags), int)
        self.assertEqual(type(attempts), int)

    def test_incorrect_get_coords_of_angle(self):
        self.assertRaises(InappropriateArgsError, self.field._get_coords_of_angle, 1)
        self.assertRaises(InappropriateArgsError, self.field._get_coords_of_angle, "1")

    def test_correct_get_coords_of_angle(self):
        lines = self.field._get_hough_lines(self.field.changing_img)
        result = self.field._get_coords_of_angle(lines)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(Validator.is_number(result[0].tolist()), True)

    def test_incorrect_run_kmeans_on_coords(self):
        lines = self.field._get_hough_lines(self.field.changing_img)
        self.assertRaises(InappropriateArgsError, self.field._run_kmeans_on_coords, lines, "1")
        self.assertRaises(InappropriateArgsError, self.field._run_kmeans_on_coords, lines, -1)
        self.assertRaises(InappropriateArgsError, self.field._run_kmeans_on_coords, "Not even close.", 1)
        self.assertRaises(InappropriateArgsError, self.field._run_kmeans_on_coords, 1, "1")

    def test_correct_run_kmeans_on_coords(self):
        result = self.field._run_kmeans_on_coords(self.field._get_hough_lines(self.field.changing_img), 2)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(Validator.is_type(result.tolist(), int), True)

    def test_incorrect_seperate_lines(self):
        self.assertRaises(InappropriateArgsError, self.field._seperate_lines, "lines")
        self.assertRaises(InappropriateArgsError, self.field._seperate_lines, 3)
        self.assertRaises(InappropriateArgsError, self.field._seperate_lines, np.ndarray, k=-1)
        self.assertRaises(InappropriateArgsError, self.field._seperate_lines, np.ndarray, k="1")

    def test_correct_seperate_lines(self):
        lines = self.field._get_hough_lines(self.field.changing_img)
        result = self.field._seperate_lines(lines)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), list)
        self.assertEqual(type(result[1]), list)
        self.assertEqual(type(result[0][0]), np.ndarray)
        self.assertEqual(type(result[1][0]), np.ndarray)

    def test_incorrect_prepare_image_for_extracting(self):
        self.assertRaises(InappropriateArgsError, self.field._prepare_image_for_extracting, 1)
        self.assertRaises(InappropriateArgsError, self.field._prepare_image_for_extracting, "Not an image")

    def test_correct_prepare_image_for_extracting(self):
        output = self.field._prepare_image_for_extracting(self.field.changing_img)
        self.assertNotEqual(np.all(self.field.img), np.all(output))
        self.field.img = cv2.GaussianBlur(self.field.img, (11, 11), 0)
        cv2.adaptiveThreshold(self.field.img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2, dst=self.field.img)
        self.field.img = cv2.bitwise_not(self.field.img)
        self.field.img = cv2.dilate(self.field.img, self.field.kernel)
        self.assertEqual(np.all(self.field.img), np.all(output))

    def test_incorrect_set_image(self):
        wrong_path = "This doesnt exists.really!"
        wrong_path1 = 3
        self.assertRaises(FileNotFoundError, lambda: ExtractField(wrong_path))
        self.assertRaises(InappropriateArgsError, lambda: ExtractField(wrong_path1))

    def test_correct_set_image(self):
        origin = cv2.imread(self.path, 0)
        field1 = ExtractField(origin)
        self.assertEqual(np.all(self.field.img), np.all(origin))
        self.assertEqual(np.all(field1.img), np.all(origin))

    def test_init(self):
        self.assertEqual(type(self.field.img), np.ndarray)
        self.assertEqual(self.field.width, 558)
        self.assertEqual(self.field.height, 563)
        self.assertEqual(type(self.field.changing_img), np.ndarray)
        self.assertEqual(type(self.field.kernel), np.ndarray)
        self.assertEqual(len(self.field.kernel), 3)
        self.assertEqual(len(self.field.kernel[0]), 3)
        self.assertEqual(len(self.field.kernel[1]), 3)
        self.assertEqual(len(self.field.kernel[2]), 3)
