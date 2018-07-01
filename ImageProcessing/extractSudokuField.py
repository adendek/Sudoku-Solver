from Common.Errors import InappropriateArgsError, SudokuFieldSizeError
from Common.validationFunctions import Validator
from collections import defaultdict
import numpy as np
import cv2
import math
import os


class ExtractField:
    def __init__(self, source):
        self.img = self._set_image(source)
        self.height, self.width = self.img.shape[:2]
        self.changing_img = self.img
        self.kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
        self.changing_img = self._prepare_image_for_extracting(self.changing_img)
        self._expose_biggest_blob()

    def _set_image(self, source):
        if isinstance(source, str) and os.path.exists(source):  # load picture from the path
            self.img = cv2.imread(source, 0)  # gray scale
            return self.img
        elif isinstance(source, np.ndarray):  # source is image
            self.img = source
            if len(source.shape) == 3:  # it is in RGB not in gray scale
                self.img = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)  # transform image to gray scale
            return self.img
        elif isinstance(source, str) and not os.path.exists(source):  # invalid path
            raise FileNotFoundError("File does not exists: " + source)
        else:  # other cases are invalid
            raise InappropriateArgsError("extracting a sudoku field: " + str(source))

    def _prepare_image_for_extracting(self, image):
        if isinstance(image, np.ndarray):
            image = cv2.GaussianBlur(image, (11, 11), 0)  # smooths out the noise a bit
            # based on the illumination it "resharpens" objects
            cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2, dst=image)
            image = cv2.bitwise_not(image)  # inverts every bit - changes black and white
            image = cv2.dilate(image, self.kernel)
            return image
        raise InappropriateArgsError("preparing image for extracting: " + str(image))

    def _seperate_lines(self, lines, k=2, **kwargs):
        """
        Groups lines based on angle with k-means.
        Uses k-means on the coordinates of the angle on the unit circle
        to segment `k` angles inside `lines`.
        The result is separation of vertical and horizontal lines.
        """
        if Validator.is_type(lines, np.ndarray) and Validator.is_positive_number(k) and Validator.is_type(k, int):
            labels = self._run_kmeans_on_coords(lines, k, **kwargs)
            # separate lines based on their k-means label
            separated = defaultdict(list)
            for i, line in zip(range(len(lines)), lines):
                separated[labels[i]].append(line)
            return list(separated.values())
        raise InappropriateArgsError("seperating vertical and horizontal lines")

    def _run_kmeans_on_coords(self, lines, k, **kwargs):
        if Validator.is_type(lines, np.ndarray) and Validator.is_positive_number(k) and Validator.is_type(k, int):
            # Define criteria = (type, max_iter, epsilon)
            criteria, flags, attempts = self._get_criteria_flags_attempts(**kwargs)
            pts = self._get_coords_of_angle(lines)
            # run k-means on the coordinates
            labels, centers = cv2.kmeans(pts, k, None, criteria, attempts, flags)[1:]
            return labels.reshape(-1)  # transpose to row vector
        raise InappropriateArgsError("running k-means on coordinates: " + str(lines))

    def _get_coords_of_angle(self, lines):
        if Validator.is_type(lines, np.ndarray):
            angles = np.array([line[0][1] for line in lines])  # returns angles in [0, pi] in radians
            # multiply the angles by two and find coordinates of that angle
            return np.array([[np.cos(2 * angle), np.sin(2 * angle)] for angle in angles], dtype=np.float32)
        raise InappropriateArgsError("getting the coordinates of the angles" + str(lines))

    def _get_criteria_flags_attempts(self, **kwargs):
        default_criteria_type = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
        criteria = kwargs.get('criteria', (default_criteria_type, 10, 1.0))
        flags = kwargs.get('flags', cv2.KMEANS_RANDOM_CENTERS)
        attempts = kwargs.get('attempts', 10)
        return criteria, flags, attempts

    def _get_intersection_point(self, line1, line2):
        """
        Finds the intersection of two lines given in Hesse normal form.
        Returns closest integer pixel locations.
        """
        if Validator.is_type([line1, line2], np.ndarray):
            rho1, theta1 = line1[0]
            rho2, theta2 = line2[0]
            a = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
            b = np.array([[rho1], [rho2]])
            x0, y0 = np.linalg.solve(a, b)
            return int(np.round(x0)), int(np.round(y0))
        raise InappropriateArgsError("finding the intersection between lines: " + str(line1) + " and " + str(line2))

    def _get_points_on_line(self, rho, theta):
        if Validator.is_number([rho, theta]):
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            return int(x0 + 1000 * (- b)), int(y0 + 1000 * a), int(x0 - 1000 * (- b)), int(y0 - 1000 * a)
        raise InappropriateArgsError("getting points with rho: " + str(rho) + " and theta: " + str(theta))

    def _get_corner_points(self):
        # top_left_point, top_right_point, bottom_left_point, bottom_right_point
        tl_pt, tr_pt, bl_pt, br_pt = self._init_points()
        separated = self._seperate_lines(self._get_hough_lines(self.changing_img))
        self.changing_img = cv2.erode(self.changing_img, self.kernel)  # more accuracy - thinner white line of blob
        for line in separated[0]:  # horizontals
            for line2 in separated[1]:  # verticals
                x, y = self._get_intersection_point(line, line2)
                if 0 < x < self.width and 0 < y < self.height:  # intersection is in the area of the image
                    tl_pt, tr_pt, bl_pt, br_pt = self._update_corners(x, y, tl_pt, tr_pt, bl_pt, br_pt)
        return tl_pt, tr_pt, bl_pt, br_pt

    def _update_corners(self, x, y, tl_point, tr_point, bl_point, br_point):
        if Validator.is_positive_number([x, y]) and Validator.is_type([tl_point, tr_point, bl_point, br_point], tuple):
            color = self.changing_img[y][x]  # color of that pixel, if it is white (255) we are on the blob
            if x + y < tl_point[0] + tl_point[1] and color == 255:  # point is more upper-left than the current one
                tl_point = x, y
            if y - x > bl_point[1] - bl_point[0] and color == 255:  # point is more bottom-left than the current one
                bl_point = x, y
            if x - y > tr_point[0] - tr_point[1] and color == 255:  # point is more top-right than the current one
                tr_point = x, y
            if x + y > br_point[0] + br_point[1] and color == 255:  # point is more bottom-right than the current one
                br_point = x, y
            return tl_point, tr_point, bl_point, br_point
        raise InappropriateArgsError("updating corner points with x: " + str(x) + " and y: " + str(y))

    def _init_points(self):
        # returns the worst case scenario points
        return (self.width, self.height), (0, self.height), (self.width, 0), (0, 0)

    def _get_distance_between_points(self, p1, p2):
        if Validator.is_type([p1, p2], tuple) and Validator.is_number([p1[0], p1[1], p2[0], p2[1]]):
            return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        raise InappropriateArgsError("calculating distance between points p1: " + str(p1) + " and p2: " + str(p2))

    def draw_point(self, img, pt):
        if Validator.is_type(img, np.ndarray) and Validator.is_type(pt, tuple) and Validator.is_number([pt[0], pt[1]]):
            cv2.circle(img, pt, 5, (0, 0, 255, 0), 2)
        raise InappropriateArgsError("drawing a point: " + str(pt) + " to image: " + str(img))

    def extract_sudoku_field(self):
        # returns the picture which includes entire sudoku field
        tl, tr, bl, br = self._get_corner_points()
        size = round(self._get_longest_line(tl, tr, bl, br))
        src = np.array([tl, tr, bl, br], np.float32)
        dst = np.array([(0, 0), (size-1, 0), (0, size-1), (size-1, size-1)], np.float32)
        matrix = cv2.getPerspectiveTransform(src, dst)
        return cv2.warpPerspective(self.img, matrix, (size, size))

    def _get_longest_line(self, tl, tr, bl, br):
        if Validator.is_type([tl, tr, bl, br], tuple) and \
                Validator.is_number([tl[0], tl[1], tr[0], tr[1], bl[0], bl[1], br[0], br[1]]):
            tltr = self._get_distance_between_points(tl, tr)
            tlbl = self._get_distance_between_points(tl, bl)
            trbr = self._get_distance_between_points(tr, br)
            blbr = self._get_distance_between_points(bl, br)
            max_value = max([tltr, tlbl, trbr, blbr])  # returns the max value of the list
            min_value = min([tltr, tlbl, trbr, blbr])  # returns the min value of the list
            if max_value - min_value > max_value * 0.1:  # if the difference is grater than 10 % of max value
                raise SudokuFieldSizeError()  # one corner wasn't detected so we should try it again
            return max_value
        raise InappropriateArgsError("calculating the longest line")

    def _get_hough_lines(self, img):
        if Validator.is_type(img, np.ndarray):
            return cv2.HoughLines(img, 1, np.pi / 180, 200)
        raise InappropriateArgsError("getting hough lines on image: " + str(img))

    def _expose_biggest_blob(self):
        """
        The goal of this function is to find the biggest blob - hopefully this is the sudoku field square
        """
        max = -1
        max_point = None
        for y in range(self.height):
            row = self.changing_img[y]
            for x in range(self.width):
                if row[x] > 128:  # only white parts are flooded
                    area = cv2.floodFill(self.changing_img, None, (x, y), 64)[0]  # fills the blob area to gray
                    if area > max:  # area = how big the blob is
                        max = area
                        max_point = (x, y)
        cv2.floodFill(self.changing_img, None, max_point, (255, 255, 255))  # fills the max blob area to white
        return self._hide_smaller_blobs(max_point)  # hide all areas that are gray - are not the biggest ones

    def _hide_smaller_blobs(self, max_point):
        if Validator.is_type(max_point, tuple) and Validator.is_positive_number([max_point[0], max_point[1]]):
            for y in range(self.height):
                row = self.changing_img[y]
                for x in range(self.width):
                    if row[x] == 64 and max_point[0] != x and max_point[1] != y:  # fills gray parts with black
                        cv2.floodFill(self.changing_img, None, (x, y), 0)
            return True
        raise InappropriateArgsError("hiding smaller blobs with point: " + str(max_point))

    def show_result(self):
        # show what is the result -> should be only sudoku field
        result = self.extract_sudoku_field()
        cv2.imshow("result", result)
        cv2.waitKey(0)
        return result

    def show_blob(self):
        # shows the biggest blob in the picture -> outline of sudoku field
        cv2.imshow("blob.jpg", self.changing_img)
        cv2.waitKey(0)
        return self.changing_img

    def show_source(self):
        # shows source image
        cv2.imshow('source.jpg', self.img)
        cv2.waitKey(0)
        return self.img
