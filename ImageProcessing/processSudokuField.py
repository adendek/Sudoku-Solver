from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
from MachineLearning.char74kClassify import Char74kClassify
import numpy as np
import cv2


class ProcessSudokuField:
    def __init__(self, pure_sudoku_field):
        if Validator.is_type(pure_sudoku_field, np.ndarray):
            self.img = pure_sudoku_field
            self.sudoku_size = 9
            self.height, self.width = self._get_height_width(self.img)
            self.error = self.width // 200  # some lines are thicker than others
            self.cut_border = 3  # try to avoid border lines of the square with the number
            self.model = Char74kClassify()
            if self.height != self.width:
                raise InappropriateArgsError("processing sudoku field! The height and width are not matching")
        else:
            raise InappropriateArgsError("processing sudoku field input: " + str(pure_sudoku_field))

    def process_field_and_get_number_matrix(self, draw_grid=False):
        if Validator.is_type(draw_grid, bool):
            padding = self._get_grid_padding()
            field = []
            y_error = 0
            for y in range(self.sudoku_size):
                field.append([])
                y_error = self._update_error(y, y_error)
                self._draw_lines_if_true(y, padding, y_error, draw_grid)
                x_error = 0
                for x in range(self.sudoku_size):
                    img = self._get_image_from_coords(x_error, x, y_error, y, padding)
                    field[y].append(int(self._get_number(img)))
            return field
        raise InappropriateArgsError("processing image and getting its matrix! arg: " + str(draw_grid))

    def _get_number(self, img):
        if Validator.is_type(img, np.ndarray):
            img = self._prepare_image_for_recognizing_or_return_0(img)
            if Validator.is_type(img, int) and img == 0:
                return 0
            return int(self.model.classify_image(img))  # TODO: change classifier
        raise InappropriateArgsError("getting a number! arg: " + str(img))

    def _prepare_image_for_recognizing_or_return_0(self, img):
        if not Validator.is_type(img, np.ndarray):
            raise InappropriateArgsError("preparing image for recognition! arg: " + str(img))
        working_img, original = self._get_transformed_img_and_original(img)
        contours = self._get_contours(working_img)
        if contours:
            x, y, width, height = self._get_x_y_width_height_from_contours(contours)
            higher, lower, diff = self._get_higher_lower_diff(width, height)
            if 20 < diff < 90 and height > 7 and width > 7:  # some parameters that tries to separate edges from numbers
                original = self._prepare_original_for_recognition(original, height, width, x, y, self._get_kernel(3, 3))
                return self._change_image_like_training_images(original, working_img.shape[1], working_img.shape[0])
        return 0  # square is not containing any number

    def _get_image_from_coords(self, x_error, x, y_error, y, padding):
        if Validator.is_positive_number([x_error, x, y_error, y, y_error, padding]) and \
                Validator.is_type([x, y, x_error, y_error, padding], int):
            x1, y1, x2, y2 = self._get_tr_bl_corners_of_little_square(x_error, x, y_error, y, padding)
            return self._extract_field_square_with_number_image(x1, y1, x2, y2)
        raise InappropriateArgsError("getting image from coors!")

    def _get_x_y_width_height_from_contours(self, contours):
        if Validator.is_type(contours, np.ndarray):
            return cv2.boundingRect(sorted(contours, key=cv2.contourArea)[-1])
        raise InappropriateArgsError("getting x, y, width, height from contours (" + str(contours) + ")")

    def _get_contours(self, img):
        if Validator.is_type(img, np.ndarray):
            return cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        raise InappropriateArgsError("getting contours! " + str(img))

    def _prepare_original_for_recognition(self, img, height, width, x, y, kernel):
        # thicker the number and extract it (hopefully)
        if Validator.is_type([img, kernel], np.ndarray) and Validator.is_positive_number([height, width, x, y]):
            original = cv2.erode(img, kernel)
            return original[y:y + height, x:x + width]
        raise InappropriateArgsError("preparing image for recognition!")

    def _get_higher_lower_diff(self, width, height):
        if Validator.is_positive_number([width, height]):
            higher, lower = max(width, height), min(width, height)
            diff = lower * 100
            if higher > 0:
                diff = (lower / higher) * 100
            return higher, lower, diff
        raise InappropriateArgsError("getting higher lower difference")

    def _get_kernel(self, height, width):
        if Validator.is_positive_number([height, width]) and Validator.is_type([height, width], int):
            return np.ones((height, width), np.uint8)
        raise InappropriateArgsError("getting kernel")

    def _get_transformed_img_and_original(self, working_img):
        if not Validator.is_type(working_img, np.ndarray):
            raise InappropriateArgsError("getting transformed img and original! arg:" + str(working_img))
        working_img = cv2.GaussianBlur(working_img, (13, 13), 0)  # smooths out the noise
        cv2.adaptiveThreshold(working_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2, dst=working_img)
        working_img = cv2.bitwise_not(working_img)   # only white and black
        original = cv2.bitwise_not(working_img)
        kernel = self._get_kernel(3, 3)
        working_img = cv2.dilate(working_img, kernel)
        return working_img, original

    def _get_offset(self, width, height, smaller_height, smaller_width):
        if Validator.is_positive_number([width, height, smaller_width, smaller_height]):
            return (width - smaller_width) // 2, (height - smaller_height) // 2
        raise InappropriateArgsError("getting the offset")

    def _change_image_like_training_images(self, image, width, height):
        # this function adds white corners around the digit. The image is then more similar to the training set images!
        if Validator.is_positive_number([width, height]) and Validator.is_type([width, height], int) and \
                Validator.is_type(image, np.ndarray) and width >= image.shape[1] and height >= image.shape[0]:
            new_img = self._create_white_picture(width, height)  # completely white
            smaller_height, smaller_width = self._get_height_width(image)
            x_offset, y_offset = self._get_offset(width, height, smaller_height, smaller_width)
            new_img[y_offset:y_offset + smaller_height, x_offset:x_offset + smaller_width] = image
            return new_img
        raise InappropriateArgsError("changing image like training images!")

    def _get_height_width(self, image):
        if Validator.is_type(image, np.ndarray):
            return image.shape[:2]
        raise InappropriateArgsError("getting height and width from image (" + str(image) + ")")

    def _create_white_picture(self, width, height):
        if Validator.is_positive_number([width, height]) and Validator.is_type([width, height], int):
            img = np.zeros((height, width), dtype=np.uint8)
            img.fill(255)  # must be white
            return img
        raise InappropriateArgsError("creating white picture")

    def _get_cropped_tl_br_point(self, x1, y1, x2, y2):
        if Validator.is_positive_number([x1, y1, x2, y2]):
            return (x1 + self.cut_border, y1 + self.cut_border), (x2 - self.cut_border, y2 - self.cut_border)
        raise InappropriateArgsError("getting cropped top-left bottom-right point")

    def _extract_field_square_with_number_image(self, x1, y1, x2, y2):
        if Validator.is_positive_number([x1, y1, x2, y2]) and Validator.is_type([x1, y1, x2, y2], int):
            p1, p4 = self._get_cropped_tl_br_point(x1, y1, x2, y2)
            r = cv2.boundingRect(np.array([[p1[0], p1[1]], [p4[0], p4[1]]]))
            return self.img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
        raise InappropriateArgsError("extracting field square with number image")

    def _calculate_x_y(self, x, y, x_error, y_error, padding):
        if Validator.is_positive_number([x, y, x_error, y_error, padding]):
            return x * padding + x_error, y * padding + y_error
        raise InappropriateArgsError("calculating x and y")

    def _get_tr_bl_corners_of_little_square(self, x_error, x, y_error, y, padding):
        if Validator.is_positive_number([x, y, x_error, y_error, padding]):
            x_error = self._update_error(x, x_error)
            x1, y1 = self._calculate_x_y(x, y, x_error, y_error, padding)
            next_point_error = self._update_error(x + 1, x_error)
            return x1, y1, x1 + padding + next_point_error, y1 + padding + y_error
        raise InappropriateArgsError("getting top-right and bottom-left corners of little square")

    def _draw_lines_if_true(self, y, padding, y_error, draw):
        if not (Validator.is_positive_number([y, padding, y_error]) and Validator.is_type(draw, bool)):
            raise InappropriateArgsError("drawing lines")
        if draw:
            self._draw_line(0, padding * y + y_error, self.width, padding * y + y_error)
            self._draw_line(padding * y + y_error, 0, padding * y + y_error, self.height)
            return True
        return False

    def _draw_line(self, x1, y1, x2, y2):
        if Validator.is_positive_number([x1, y1, x2, y2]):
            return cv2.line(self.img, (x1, y1), (x2, y2), (255, 255, 255))
        raise InappropriateArgsError("drawing the line")

    def _update_error(self, line, error):
        if not Validator.is_positive_number([line, error]):
            raise InappropriateArgsError("updating error")
        if line != 0 and self.sudoku_size % line == 0:  # increase err when there is a thicker line (3, 6 for 9x9 field)
            return error + self.error
        return error

    def _get_grid_padding(self):
        return self.width // self.sudoku_size

    def draw_grid(self):
        return self.process_field_and_get_number_matrix(draw_grid=True)

    def show_field(self):
        cv2.imshow('Detected field.jpg', self.img)
        cv2.waitKey(0)
