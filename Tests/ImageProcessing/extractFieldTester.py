from Common.Errors import InappropriateArgsError
from Common.validationFunctions import Validator
from ImageProcessing.extractField import ExtractField
from Tests.ImageProcessing.processImageTester import PATH
from unittest import TestCase
import numpy as np
import cv2


class ExtractFieldTester(TestCase):
    def test_incorrect_hide_smaller_blobs(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._hide_smaller_blobs(1))
        self.assertRaises(InappropriateArgsError, lambda: field._hide_smaller_blobs("1"))

    def test_incorrect_hough_lines(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._get_hough_lines(1))
        self.assertRaises(InappropriateArgsError, lambda: field._get_hough_lines("1"))

    def test_get_hough_lines(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        result = field._get_hough_lines(field.changing_img)
        self.assertEqual(type(result), np.ndarray)

    def test_incorrect_get_longest_line(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        ok = (1, 1)
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(1, ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line("1", ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(ok, 1, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(ok, "1", ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(ok, ok, 1, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(ok, ok, "1", ok))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(ok, ok, ok, 1))
        self.assertRaises(InappropriateArgsError, lambda: field._get_longest_line(ok, ok, ok, "1"))

    def test_correct_get_longest_line(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        tl, tr, bl = (0, 0), (0, 0), (0, 0)
        br = (0, 100)
        self.assertEqual(type(field._get_longest_line(tl, tr, bl, br)), float)
        self.assertEqual(field._get_longest_line(tl, tr, bl, br), 100)

    def test_incorrect_draw_point(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        ok_point = (1, 1)
        ok_img = field.img
        self.assertRaises(InappropriateArgsError, lambda: field.draw_point("false", ok_point))
        self.assertRaises(InappropriateArgsError, lambda: field.draw_point(ok_img, "1"))

    def test_incorrect_distance_between_points(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._get_distance_between_points(1, (3, -4)))
        self.assertRaises(InappropriateArgsError, lambda: field._get_distance_between_points((1, 1), 3))
        self.assertRaises(InappropriateArgsError, lambda: field._get_distance_between_points("1", (3, -4)))
        self.assertRaises(InappropriateArgsError, lambda: field._get_distance_between_points((1, 1), "1"))

    def get_correct_distance_between_points(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        result = field._get_distance_between_points((-1, 3), (3, -4))
        self.assertEqual(type(result), float)
        self.assertGreater(result, 0)
        self.assertEqual(result, 8.026)

    def test_init_points(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        result = field._init_points()
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 4)
        correct_result = ((field.width, field.height), (0, field.height), (field.width, 0), (0, 0))
        self.assertEqual(result, correct_result)

    def test_incorrect_update_corners(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        ok = (1, 1)
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners("1", 1, ok, ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(-1, 1, ok, ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(1, "1", ok, ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(-1, 1, ok, ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(-1, 1, 1, ok, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(-1, 1, ok, 1, ok, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(-1, 1, ok, ok, 1, ok))
        self.assertRaises(InappropriateArgsError, lambda: field._update_corners(-1, 1, ok, ok, ok, 1))

    def test_correct_update_corners(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        tl, tr, bl, bt = (100, 100), (100, 100), (100, 100), (100, 100)
        result = field._update_corners(1, 1, tl, tr, bl, bt)
        self.assertEqual(result, (tl, tr, bl, bt))  # shouldn't change anything
        result = field._update_corners(74, 84, tl, tr, bl, bt)
        self.assertNotEqual(result, (tl, tr, bl, bt))

    def test_corner_points(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        result = field._get_corner_points()
        self.assertEqual(len(result), 4)
        self.assertEqual(type(result), tuple)
        self.assertEqual(Validator.is_positive_number(list(result[0])), True)
        self.assertEqual(Validator.is_positive_number(list(result[1])), True)
        self.assertEqual(Validator.is_positive_number(list(result[2])), True)
        self.assertEqual(Validator.is_positive_number(list(result[3])), True)
        self.assertEqual(result, ((74, 84), (492, 70), (37, 512), (520, 520)))

    def test_incorrect_get_points_on_line(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._get_points_on_line(1, "1"))
        self.assertRaises(InappropriateArgsError, lambda: field._get_points_on_line("1", 1))

    def test_correct_get_points_on_line(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        result = field._get_points_on_line(3, 3)
        self.assertEqual(type(result), tuple)
        self.assertEqual(Validator.is_number(list(result)), True)
        self.assertEqual(result, (-144, -989, 138, 990))

    def test_incorrect_get_intersection_points(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        lines = field._seperate_lines(field._get_hough_lines(field.changing_img))
        line = lines[0]
        self.assertRaises(InappropriateArgsError, lambda: field._get_intersection_point(line, 1))
        self.assertRaises(InappropriateArgsError, lambda: field._get_intersection_point(line, "1"))
        self.assertRaises(InappropriateArgsError, lambda: field._get_intersection_point(1, line))
        self.assertRaises(InappropriateArgsError, lambda: field._get_intersection_point("1", line))

    def test_correct_get_intersection_points(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        lines = field._seperate_lines(field._get_hough_lines(field.changing_img))
        line1 = lines[0][0]
        line2 = lines[1][0]
        result = field._get_intersection_point(line1, line2)
        self.assertEqual(type(result), tuple)
        self.assertEqual(type(result[0]), int)
        self.assertEqual(type(result[1]), int)
        self.assertEqual(result, (520, 520))

    def test_correct_get_criteria_flags_attempts(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        criteria, flags, attempts = field._get_criteria_flags_attempts()
        self.assertEqual(type(criteria), tuple)
        self.assertEqual(len(criteria), 3)
        self.assertEqual(type(flags), int)
        self.assertEqual(type(attempts), int)

    def test_incorrect_get_coords_of_angle(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._get_coords_of_angle(1))
        self.assertRaises(InappropriateArgsError, lambda: field._get_coords_of_angle("1"))

    def test_correct_get_coords_of_angle(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        lines = field._get_hough_lines(field.changing_img)
        result = field._get_coords_of_angle(lines)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(Validator.is_number(result[0].tolist()), True)

    def test_incorrect_run_kmeans_on_coords(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        lines = field._get_hough_lines(field.changing_img)
        self.assertRaises(InappropriateArgsError, lambda: field._run_kmeans_on_coords(lines, "1"))
        self.assertRaises(InappropriateArgsError, lambda: field._run_kmeans_on_coords(lines, -1))
        self.assertRaises(InappropriateArgsError, lambda: field._run_kmeans_on_coords("Not even close.", 1))
        self.assertRaises(InappropriateArgsError, lambda: field._run_kmeans_on_coords(1, "1"))

    def test_correct_run_kmeans_on_coords(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        result = field._run_kmeans_on_coords(field._get_hough_lines(field.changing_img), 2)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(Validator.is_type(result.tolist(), int), True)

    def test_incorrect_seperate_lines(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._seperate_lines("lines"))
        self.assertRaises(InappropriateArgsError, lambda: field._seperate_lines(3))
        self.assertRaises(InappropriateArgsError, lambda: field._seperate_lines(np.ndarray, k=-1))
        self.assertRaises(InappropriateArgsError, lambda: field._seperate_lines(np.ndarray, k="1"))

    def test_correct_seperate_lines(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        lines = field._get_hough_lines(field.changing_img)
        result = field._seperate_lines(lines)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), list)
        self.assertEqual(type(result[1]), list)
        self.assertEqual(type(result[0][0]), np.ndarray)
        self.assertEqual(type(result[1][0]), np.ndarray)

    def test_incorrect_prepare_image_for_extracting(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        self.assertRaises(InappropriateArgsError, lambda: field._prepare_image_for_extracting(1))
        self.assertRaises(InappropriateArgsError, lambda: field._prepare_image_for_extracting("Not an image"))

    def test_correct_prepare_image_for_extracting(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        field = ExtractField(path)
        output = field._prepare_image_for_extracting(field.changing_img)
        self.assertNotEqual(np.all(field.img), np.all(output))
        field.img = cv2.GaussianBlur(field.img, (11, 11), 0)
        cv2.adaptiveThreshold(field.img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2, dst=field.img)
        field.img = cv2.bitwise_not(field.img)
        field.img = cv2.dilate(field.img, field.kernel)
        self.assertEqual(np.all(field.img), np.all(output))

    def test_incorrect_set_image(self):
        wrong_path = "This doesnt exists.really!"
        wrong_path1 = 3
        self.assertRaises(FileNotFoundError, lambda: ExtractField(wrong_path))
        self.assertRaises(InappropriateArgsError, lambda: ExtractField(wrong_path1))

    def test_correct_set_image(self):
        path = PATH + "/../../SamplePictures/sudoku.jpg"
        origin = cv2.imread(path, 0)
        field = ExtractField(path)
        field1 = ExtractField(origin)
        self.assertEqual(np.all(field.img), np.all(origin))
        self.assertEqual(np.all(field1.img), np.all(origin))

    def test_init(self):
        field = ExtractField(PATH + "/../../SamplePictures/sudoku.jpg")
        self.assertEqual(type(field.img), np.ndarray)
        self.assertEqual(field.width, 558)
        self.assertEqual(field.height, 563)
        self.assertEqual(type(field.changing_img), np.ndarray)
        self.assertEqual(type(field.kernel), np.ndarray)
        self.assertEqual(len(field.kernel), 3)
        self.assertEqual(len(field.kernel[0]), 3)
        self.assertEqual(len(field.kernel[1]), 3)
        self.assertEqual(len(field.kernel[2]), 3)
