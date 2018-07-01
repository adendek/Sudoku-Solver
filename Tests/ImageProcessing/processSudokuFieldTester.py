from ImageProcessing.processSudokuField import ProcessSudokuField
from Tests.ImageProcessing.extractSudokuFieldTester import PATH
from ImageProcessing.extractSudokuField import ExtractField
from Common.Errors import InappropriateArgsError
from Common.validationFunctions import Validator
from unittest import TestCase
import numpy as np
import cv2


class ProcessSudokuFieldTester(TestCase):
    def setUp(self):
        self.path = PATH + "/../../SamplePictures/sudokuNice.jpg"
        self.field = ExtractField(self.path).extract_sudoku_field()
        self.process = ProcessSudokuField(self.field)
        
    def test_draw_grid(self):
        
        before = self.process.img.copy()
        result = self.process.draw_grid()
        self.assertEqual(np.array_equal(before, self.process.img), False)
        self.assertEqual(Validator.is_9x9_integers_field(result), True)

    def test_correct_get_grid_padding(self):
        self.assertEqual(self.process._get_grid_padding(), self.process.width // self.process.sudoku_size)

    def test_incorrect_update_error(self):
        self.assertRaises(InappropriateArgsError, self.process._update_error, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._update_error, 1, -1)
        self.assertRaises(InappropriateArgsError, self.process._update_error, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._update_error, 1, "1")

    def test_correct_update_error(self):
        self.assertEqual(self.process._update_error(0, 1), 1)
        self.assertEqual(self.process._update_error(3, 1), 2)

    def test_incorrect_draw_line(self):
        self.assertRaises(InappropriateArgsError, self.process._draw_line, -1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._draw_line, 1, "1", 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._draw_line, 1, 1, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._draw_line, 1, 1, 1, "1")

    def test_correct_draw_line(self):
        before = self.process.img.copy()
        self.assertEqual(np.array_equal(before, self.process.img), True)
        self.assertEqual(type(self.process._draw_line(1, 1, 10, 10)), np.ndarray)
        self.assertEqual(np.array_equal(before, self.process.img), False)

    def test_incorrect_draw_lines_if_true(self):
        self.assertRaises(InappropriateArgsError, self.process._draw_lines_if_true, "1", 0, 0, True)
        self.assertRaises(InappropriateArgsError, self.process._draw_lines_if_true, 0, -1, 0, True)
        self.assertRaises(InappropriateArgsError, self.process._draw_lines_if_true, 0, 0, "1", True)
        self.assertRaises(InappropriateArgsError, self.process._draw_lines_if_true, 0, 0, 0, "1")

    def test_correct_draw_lines_if_true(self):
        before = self.process.img.copy()
        self.assertEqual(False, self.process._draw_lines_if_true(0, 10, 0, False))
        self.assertEqual(np.array_equal(before, self.process.img), True)
        self.assertEqual(True, self.process._draw_lines_if_true(1, 10, 1, True))
        self.assertEqual(np.array_equal(before, self.process.img), False)

    def test_incorrect_get_tr_bl_corners_of_little_square(self):
        self.assertRaises(InappropriateArgsError, self.process._get_tr_bl_corners_of_little_square, -1, 1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_tr_bl_corners_of_little_square, 1, "1", 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_tr_bl_corners_of_little_square, 1, 1, -1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_tr_bl_corners_of_little_square, 1, 1, 1, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._get_tr_bl_corners_of_little_square, 1, 1, 1, 1, -1)

    def test_correct_get_tr_bl_corners_of_little_square(self):
        result = self.process._get_tr_bl_corners_of_little_square(0, 0, 0, 0, 10)
        self.assertEqual(result, (0, 0, 11, 10))

    def test_incorrect_calculate_x_y(self):
        self.assertRaises(InappropriateArgsError, self.process._calculate_x_y, -1, 1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._calculate_x_y, 1, "1", 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._calculate_x_y, 1, 1, -1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._calculate_x_y, 1, 1, 1, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._calculate_x_y, 1, 1, 1, 1, -1)

    def test_correct_calculate_x_y(self):
        self.assertEqual(self.process._calculate_x_y(0, 0, 0, 0, 10), (0, 0))
        self.assertEqual(self.process._calculate_x_y(1, 2, 2, 2, 10), (12, 22))

    def test_incorrect_extract_field_square_with_number_image(self):
        self.assertRaises(InappropriateArgsError, self.process._extract_field_square_with_number_image, -1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._extract_field_square_with_number_image, 1, "1", 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._extract_field_square_with_number_image, 1, 1, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._extract_field_square_with_number_image, 1, 1, 1, "1")

    def test_correct_extract_field_square_with_number_image(self):
        result = self.process._extract_field_square_with_number_image(0, 0, 10, 10)
        self.assertEqual(type(result), np.ndarray)

    def test_incorrect_get_cropped_tl_br_point(self):
        self.assertRaises(InappropriateArgsError, self.process._get_cropped_tl_br_point, -1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_cropped_tl_br_point, 1, "1", 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_cropped_tl_br_point, 1, 1, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_cropped_tl_br_point, 1, 1, 1, "1")

    def test_correct_get_cropped_tl_br_point(self):
        result = self.process._get_cropped_tl_br_point(0, 0, 0, 0)
        correct_result_x = self.process.cut_border, self.process.cut_border
        correct_result_y = -self.process.cut_border, -self.process.cut_border
        self.assertEqual(result, (correct_result_x, correct_result_y))

    def test_incorrect_white_picture(self):
        self.assertRaises(InappropriateArgsError, self.process._create_white_picture, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._create_white_picture, 1, -1)
        self.assertRaises(InappropriateArgsError, self.process._create_white_picture, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._create_white_picture, 1, "1")

    def test_create_white_picture(self):
        result = self.process._create_white_picture(10, 10)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(result.shape, (10, 10))
        before = result
        result[result != 255] = 0  # color all pixels that are not white to black
        self.assertEqual(np.all(result), np.all(before))

    def test_incorrect_get_height_width(self):
        self.assertRaises(InappropriateArgsError, self.process._get_height_width, 0)
        self.assertRaises(InappropriateArgsError, self.process._get_height_width, "0")
        self.assertRaises(InappropriateArgsError, self.process._get_height_width, [0, 0])

    def test_correct_get_height_width(self):
        result = self.process._get_height_width(self.process.img)
        self.assertEqual(len(result), 2)
        self.assertEqual(Validator.is_positive_number(list(result)), True)
        self.assertEqual(result, (275, 275))

    def test_incorrect_change_image_like_training_images(self):
        img = self.process.img
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, "img", 500, 500)
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, 1, 500, 500)
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, [0, 0], 500, 500)
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, img, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, img, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, img, 1, "1")
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, img, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._change_image_like_training_images, img, 1, -1)

    def test_correct_change_image_like_training_images(self):
        result = self.process._change_image_like_training_images(self.process.img, 500, 500)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(result.shape, (500, 500))
        self.assertEqual(np.any(result), np.any(self.process.img))

    def test_incorrect_offset(self):
        self.assertRaises(InappropriateArgsError, self.process._get_offset, -1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_offset, 1, "1", 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_offset, 1, 1, ["1"], 1)
        self.assertRaises(InappropriateArgsError, self.process._get_offset, 1, 1, 1, [1])

    def test_correct_offset(self):
        y_offset, x_offset = self.process._get_offset(100, 100, 50, 50)
        self.assertEqual(y_offset, 25)
        self.assertEqual(x_offset, 25)

    def test_incorrect_get_transformed_img_and_original(self):
        self.assertRaises(InappropriateArgsError, self.process._get_transformed_img_and_original, 0)
        self.assertRaises(InappropriateArgsError, self.process._get_transformed_img_and_original, "1")
        self.assertRaises(InappropriateArgsError, self.process._get_transformed_img_and_original, [0, 0])

    def test_correct_get_transformed_img_and_original(self):
        img, original = self.process._get_transformed_img_and_original(self.process.img)
        self.assertEqual(type(img), np.ndarray)
        self.assertEqual(type(original), np.ndarray)
        self.assertNotEqual(np.all(self.process.img), np.all(img))
        self.assertNotEqual(np.all(self.process.img), np.all(original))

    def test_incorrect_get_kernel(self):
        self.assertRaises(InappropriateArgsError, self.process._get_kernel, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_kernel, 1.1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_kernel, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._get_kernel, 1, -1)
        self.assertRaises(InappropriateArgsError, self.process._get_kernel, 1, 1.1)
        self.assertRaises(InappropriateArgsError, self.process._get_kernel, 1, "1")

    def test_correct_get_kernel(self):
        result = self.process._get_kernel(3, 3)
        self.assertEqual(type(result), np.ndarray)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]), 3)
        self.assertEqual(len(result[2]), 3)

    def test_incorrect_get_higher_lower_diff(self):
        self.assertRaises(InappropriateArgsError, self.process._get_higher_lower_diff, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_higher_lower_diff, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._get_higher_lower_diff, 1, -1)
        self.assertRaises(InappropriateArgsError, self.process._get_higher_lower_diff, 1, "1")

    def test_correct_get_higher_lower_diff(self):
        self.assertEqual((100, 0, 0), self.process._get_higher_lower_diff(100, 0))
        self.assertEqual((50, 25, 50), self.process._get_higher_lower_diff(25, 50))
        self.assertEqual((0, 0, 0), self.process._get_higher_lower_diff(0, 0))

    def test_incorrect_prepare_original_for_recognition(self):
        kernel = self.process._get_kernel(3, 3)
        img = self.process._get_image_from_coords(self.process._update_error(3, 0), 3, 0, 0, self.process._get_grid_padding())
        x, y, width, height = self.process._get_x_y_width_height_from_contours(self.process._get_contours(img))
        self.assertRaises(InappropriateArgsError,
                          self.process._prepare_original_for_recognition, 1, height, width, x, y, kernel)
        self.assertRaises(InappropriateArgsError,
                          self.process._prepare_original_for_recognition, img, -1, width, x, y, kernel)
        self.assertRaises(InappropriateArgsError,
                          self.process._prepare_original_for_recognition, img, height, "1", x, y, kernel)
        self.assertRaises(InappropriateArgsError,
                          self.process._prepare_original_for_recognition, img, height, width, -1, y, kernel)
        self.assertRaises(InappropriateArgsError,
                          self.process._prepare_original_for_recognition, img, height, width, x, "1", kernel)
        self.assertRaises(InappropriateArgsError,
                          self.process._prepare_original_for_recognition, img, height, width, x, y, "1")

    def test_correct_prepare_original_for_recognition(self):
        kernel = self.process._get_kernel(3, 3)
        img = self.process._get_image_from_coords(self.process._update_error(3, 0), 3, 0, 0, self.process._get_grid_padding())
        x, y, width, height = self.process._get_x_y_width_height_from_contours(self.process._get_contours(img))
        output = self.process._prepare_original_for_recognition(img, height, width, x, y, kernel)
        self.assertEqual(type(output), np.ndarray)

    def test_incorrect_get_contours(self):
        self.assertRaises(InappropriateArgsError, self.process._get_contours, 0)
        self.assertRaises(InappropriateArgsError, self.process._get_contours, "0")
        self.assertRaises(InappropriateArgsError, self.process._get_contours, [0, 0])

    def test_correct_get_contours(self):
        contours = self.process._get_contours(self.process.img)
        self.assertEqual(type(contours), list)
        self.assertEqual(Validator.is_type(contours, np.ndarray), True)

    def test_incorrect_get_x_y_width_height_from_contours(self):
        self.assertRaises(InappropriateArgsError, self.process._get_x_y_width_height_from_contours, 0)
        self.assertRaises(InappropriateArgsError, self.process._get_x_y_width_height_from_contours, "1")
        self.assertRaises(InappropriateArgsError, self.process._get_x_y_width_height_from_contours, [0, 0])

    def test_get_x_y_width_height_from_contours(self):
        contours = self.process._get_contours(self.process.img)
        result = self.process._get_x_y_width_height_from_contours(contours)
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 4)
        self.assertEqual(Validator.is_positive_number(list(result)), True)
        self.assertEqual(Validator.is_type(list(result), int), True)

    def test_incorrect_get_image_from_coords(self):
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, -1, 1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, -1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, -1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1, -1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1, 1, -1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1.1, 1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1.1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1.1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1, 1.1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1, 1, 1.1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, "1", 1, 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, "1", 1, 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, "1", 1, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1, "1", 1)
        self.assertRaises(InappropriateArgsError, self.process._get_image_from_coords, 1, 1, 1, 1, "1")

    def test_correct_get_image_from_coords(self):
        self.assertEqual(type(self.process._get_image_from_coords(0, 0, 0, 0, 0)), np.ndarray)

    def test_incorrect_image_for_recognizing_or_return_0(self):
        self.assertRaises(InappropriateArgsError, self.process._prepare_image_for_recognizing_or_return_0, 0)
        self.assertRaises(InappropriateArgsError, self.process._prepare_image_for_recognizing_or_return_0, "1")
        self.assertRaises(InappropriateArgsError, self.process._prepare_image_for_recognizing_or_return_0, [0, 0])

    def test_prepare_image_for_recognizing_or_return_0(self):
        null_img = self.process._get_image_from_coords(0, 0, 0, 0, self.process._get_grid_padding())  # first square
        self.assertEqual(0, self.process._prepare_image_for_recognizing_or_return_0(null_img))
        full_img = self.process._get_image_from_coords(self.process._update_error(3, 0), 3, 0, 0, self.process._get_grid_padding())
        self.assertEqual(np.any(full_img), np.any(self.process._prepare_image_for_recognizing_or_return_0(full_img)))

    def test_incorrect_get_number(self):
        self.assertRaises(InappropriateArgsError, self.process._get_number, 1)
        self.assertRaises(InappropriateArgsError, self.process._get_number, "1")

    def test_correct_get_number(self):
        img = self.process._get_image_from_coords(0, 0, 0, 0, self.process._get_grid_padding())  # first square
        result = self.process._get_number(img)
        self.assertEqual(result, 0)
        self.assertEqual(type(result), int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, self.process.sudoku_size)

    def test_incorrect_process_field_and_get_number_matrix(self):
        self.assertRaises(InappropriateArgsError, self.process.process_field_and_get_number_matrix, draw_grid=33)
        self.assertRaises(InappropriateArgsError, self.process.process_field_and_get_number_matrix, draw_grid="1")

    def test_correct_process_field_and_get_number_matrix(self):
        result = self.process.process_field_and_get_number_matrix()
        self.assertEqual(Validator.is_9x9_integers_field(result), True)

    def test_incorrect_init(self):
        not_square_image = cv2.imread(self.path)
        self.assertRaises(InappropriateArgsError, ProcessSudokuField, 0)
        self.assertRaises(InappropriateArgsError, ProcessSudokuField, "0")
        self.assertRaises(InappropriateArgsError, ProcessSudokuField, [0, 0])
        self.assertRaises(InappropriateArgsError, ProcessSudokuField, 0)
        self.assertRaises(InappropriateArgsError, ProcessSudokuField, not_square_image)

    def test_correct_init(self):
        self.assertEqual(type(self.process.img), np.ndarray)
        self.assertEqual(np.all(self.process.img), np.all(self.field))
        self.assertEqual(self.process.sudoku_size, 9)
        self.assertEqual(self.process.height, 275)
        self.assertEqual(self.process.width, 275)
        self.assertEqual(self.process.error, self.process.width // 200)
        self.assertEqual(self.process.cut_border, 3)
