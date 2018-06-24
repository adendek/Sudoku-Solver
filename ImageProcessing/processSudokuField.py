from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
import numpy as np
import cv2


class ProcessSudokuField:
    def __init__(self, pure_sudoku_field):
        if Validator.is_type(pure_sudoku_field, np.ndarray):
            self.img = pure_sudoku_field
            self.sudoku_size = 9
            self.height, self.width = self.img.shape[:2]
            self.error = self.width // 200  # some lines are thicker than others
            self.cut_border = 2  # try to avoid border lines of the square with the number
            self.draw_grid()
            if self.height != self.width:
                raise InappropriateArgsError("processing sudoku field! The height and width are not matching")
        else:
            raise InappropriateArgsError("processing sudoku field input: " + str(pure_sudoku_field))

    def _divide_grid_on_squares(self, draw_grid=False):
        padding = self._get_grid_padding()
        y_error = 0
        for y in range(self.sudoku_size):
            y_error = self._update_error(y, y_error)
            self._draw_lines_if_true(y, padding, y_error, draw_grid)
            x_error = 0
            for x in range(self.sudoku_size):
                x1, y1, x2, y2 = self._get_square_with_number_tr_bl_corners(x_error, x, y_error, y, padding)
                img = self._extract_field_square_with_number_image(x1, y1, x2, y2)
                self._get_number(img)

    def _get_number(self, img):
        img = self._prepare_image_for_recognizing(img)
        if Validator.is_type(img, int) and img == 0:
            return 0
        cv2.imshow('number.jpg', img)
        cv2.waitKey(0)

    def _prepare_image_for_recognizing(self, img):
        img = cv2.GaussianBlur(img, (13, 13), 0)  # smooths out the noise
        cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2, dst=img)
        img = cv2.bitwise_not(img)
        original = cv2.bitwise_not(img)
        # kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
        # img = cv2.dilate(img, kernel)
        _, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contours = sorted(contours, key=cv2.contourArea)[-1]
            x, y, width, height = cv2.boundingRect(contours)  # (4) Crop and save it
            higher = max(width, height)
            lower = min(width, height)
            diff = (lower / higher) * 100
            if 20 < diff < 90 and height > 7 and width > 7:
                original = original[y:y + height, x:x + width]
                return self._change_image_like_training_images(original, img.shape[1], img.shape[0])
        return 0

    def _change_image_like_training_images(self, image, width, height):
        # this function adds white corners around the digit. The image is then more similar to the training set images!
        new_img = self._create_white_picture(width, height)  # completely white
        smaller_height, smaller_width = image.shape[:2]
        x_offset = (width - smaller_width) // 2
        y_offset = (height - smaller_height) // 2
        new_img[y_offset:y_offset + smaller_height, x_offset:x_offset + smaller_width] = image
        return new_img

    def _create_white_picture(self, width, height):
        img = np.zeros((height, width), dtype=np.uint8)
        img.fill(255)  # must be white
        return img

    def _extract_field_square_with_number_image(self, x1, y1, x2, y2):
        p1 = (x1 + self.cut_border, y1 + self.cut_border)
        p4 = (x2 - self.cut_border, y2 - self.cut_border)
        pts = np.array([[p1[0], p1[1]], [p4[0], p4[1]]])
        r = cv2.boundingRect(pts)
        return self.img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]

    def _get_square_with_number_tr_bl_corners(self, x_error, x, y_error, y, padding):
        x_error = self._update_error(x, x_error)
        x1 = x * padding + x_error
        y1 = y * padding + y_error
        next_point_error = self._update_error(x + 1, x_error)
        return x1, y1, x1 + padding + next_point_error, y1 + padding + y_error

    def _draw_lines_if_true(self, y, padding, y_error, draw):
        if draw:
            self._draw_line(0, padding * y + y_error, self.width, padding * y + y_error)
            self._draw_line(padding * y + y_error, 0, padding * y + y_error, self.height)

    def _draw_line(self, x1, y1, x2, y2):
        return cv2.line(self.img, (x1, y1), (x2, y2), (255, 255, 255))

    def _update_error(self, line, error):
        if line != 0 and self.sudoku_size % line == 0:  # increase err when there is a thicker line (3, 6 for 9x9 field)
            return error + self.error
        return error

    def _get_grid_padding(self):
        return self.width // self.sudoku_size

    def draw_grid(self):
        self._divide_grid_on_squares(draw_grid=True)

    def show_field(self):
        cv2.imshow('field.jpg', self.img)
        cv2.waitKey(0)
