from ImageProcessing.line import Line, Orientation
from ImageProcessing.numberSquare import NumberSquare
from MachineLearning import char74kClassify
from Common.Errors import InappropriateArgsError
from Common.validationFunctions import Validator
import numpy as np
import operator
import cv2
import os


class ProcessImage:
    def __init__(self, img, path=None):
        if isinstance(img, np.ndarray) or (path is not None and os.path.exists(path) and isinstance(path, str)):
            self.img = img
            if path is not None:  # we want to load from the picture path
                self.img = cv2.imread(path)
            if self.img is not None:  # self.img is set
                self.height, self.width, self.channels = self.img.shape
                self.grid_lines = self._get_main_lines()
                self.squares = self._get_field_squares()
        else:
            if path is not None and not os.path.exists(path) and isinstance(path, str):
                raise FileNotFoundError("File does not exists: " + path)
            raise InappropriateArgsError("creating a Process Image")

    def _get_hough_lines(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)  # Convert the img to gray scale
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # Apply edge detection method on the image
        return cv2.HoughLines(edges, 1, np.pi / 180, 170)

    def _get_all_lines(self):
        lines = {}
        lines[Orientation.Horizontal] = []
        lines[Orientation.Vertical] = []
        for line in self._get_hough_lines():
            r = line[0][0]
            theta = line[0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * r
            y0 = b * r
            x1 = int(x0 + 1000 * (- b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * (- b))
            y2 = int(y0 - 1000 * a)
            line = Line(x1, y1, x2, y2)
            lines[line.get_orientation()].append(line)
        return lines

    def _get_padding(self):
        # what is the minimum distance between lines
        return self.width // 18  # Based on the test pictures this is the best ratio

    def _get_main_lines(self):
        """
        Keeps only the lines that are needed (without the noise)
        :return: new Dictionary with fewer lines
        """
        max_padding = self._get_padding()  # minimum line distance (if lower the line will be thrown away)
        lines = self._get_all_lines()

        # all sorted horizontal lines
        horizontal_lines = lines[Orientation.Horizontal]
        horizontal_lines.sort(key=operator.attrgetter('y1'))

        # all sorted vertical lines
        vertical_lines = lines[Orientation.Vertical]
        vertical_lines.sort(key=operator.attrgetter('x1'))

        # place for only the "right ones"
        new_horizontal_lines = [horizontal_lines[0]]
        new_vertical_lines = [vertical_lines[0]]

        # keep only those whose distance is larger than max_padding
        for line in vertical_lines[1:]:
            if line.x1 > (new_vertical_lines[-1].x1 + max_padding):
                new_vertical_lines.append(line)

        for line in horizontal_lines[1:]:
            if line.y1 > (new_horizontal_lines[-1].y1 + max_padding):
                new_horizontal_lines.append(line)

        return {Orientation.Horizontal: new_horizontal_lines, Orientation.Vertical: new_vertical_lines}

    def _get_field_squares(self):
        squares = []
        horizontals = self.grid_lines[Orientation.Horizontal]
        verticals = self.grid_lines[Orientation.Vertical]
        for h, h_line in enumerate(horizontals):
            squares.append([])
            for v, v_line in enumerate(verticals):
                try:  # if there is no intersection it will return false, which is not iterable
                    x, y = Line.get_intersection(h_line, v_line)  # causes TypeError if False
                    if v < len(verticals) - 1 and h < len(horizontals) - 1:
                        squares[h].append(NumberSquare(v, h, (x, y)))
                    if v > 0 and h < len(horizontals) - 1:  # gives the point to the left square
                        squares[h][v - 1].add_point(x, y)  # adds the point to the previous "square"
                    if h > 0 and v < len(verticals) - 1:  # gives the point to the top square
                        squares[h - 1][v].add_point(x, y)
                    if h > 0 and v > 0:  # gives the point to the top left square
                        squares[h - 1][v - 1].add_point(x, y)
                except TypeError:
                    print("No intersection between those lines!")
        return squares[:-1]  # last one is empty - always one horizontal line to much

    def draw_lines(self):
        for orientation, lines in self.grid_lines.items():
            for line in lines:
                cv2.line(self.img, (line.x1, line.y1), (line.x2, line.y2), (0, 255, 0), 2)

    def draw_intersection_points(self):
        for line in self.squares:
            for square in line:
                p1, p2, p3, p4 = square.get_points()
                cv2.circle(self.img, p1, 3, (0, 0, 255), 5)
                cv2.circle(self.img, p2, 3, (0, 0, 255), 5)
                cv2.circle(self.img, p3, 3, (0, 0, 255), 5)
                cv2.circle(self.img, p4, 3, (0, 0, 255), 5)

    def get_field_matrix(self):
        model = char74kClassify.char74kClassify()
        matrix = []
        for line in self.squares:
            print("+---+---+---+---+---+---+---+---+---+")
            lineMatrix = []
            for i, square in enumerate(line):
                if self._image_color(self.get_image(square)) != 0:
                    predicted = model.classifyImage(self.get_image(square))
                else:
                    predicted = 0
                if predicted == 0:
                    print("|", " ", "", end="")
                else:
                    print("|", predicted, "", end="")
                lineMatrix.append(predicted)

                if i == len(line) - 1:
                    print("|")
            matrix.append(lineMatrix)
        print("+---+---+---+---+---+---+---+---+---+")
        return matrix

    def show(self):
        cv2.imshow('Detected Lines.jpg', self.img)
        cv2.waitKey(0)

    def get_image(self, square):
        if Validator.is_type(square, NumberSquare):
            p1, p2, p3, p4 = square.get_points()
            cut_border = 5
            p1 = (p1[0] + cut_border+3, p1[1] + cut_border)
            p4 = (p4[0] - cut_border, p4[1] - cut_border)
            pts = np.array([[p1[0], p1[1]], [p4[0], p4[1]]])
            r = cv2.boundingRect(pts)
            return self.img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
        else:
            raise InappropriateArgsError("getting image")

    def _image_color(self, image):
        if Validator.is_type(image, np.ndarray):
            img = image
            brown = [255, 255, 255]  # gray level
            diff = 220
            boundaries = [([brown[2] - diff, brown[1] - diff, brown[0] - diff],
                           [brown[2] + diff, brown[1] + diff, brown[0] + diff])]
            # in order BGR as opencv represents images as numpy arrays in reverse order

            for (lower, upper) in boundaries:
                lower = np.array(lower, dtype=np.uint8)
                upper = np.array(upper, dtype=np.uint8)
                mask = cv2.inRange(img, lower, upper)
                img = self._crop(img)  # output = cv2.bitwise_and(img, img, mask=mask)
                if type(img) == int:
                    return 0
                # cv2.imshow("images", img)
                # cv2.waitKey(0)
                ratio_brown = cv2.countNonZero(mask) / (img.size / 3)
                # print('brown  pixel :', ratio_brown)
                percent = np.round(ratio_brown * 100, 2)
                # print('brown pixel pexrcentage:', np.round(ratio_brown * 100, 2))
                if percent > 4:
                    return ratio_brown
                else:
                    return 0
        else:
            raise InappropriateArgsError("processing image_color")

    def _crop(self, img):
        if Validator.is_type(img, np.ndarray):
            ## (1) Convert to gray, and threshold
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

            ## (2) Morph-op to remove noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

            ## (3) Find the max-area contour
            _, cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cnts:

                cnt = sorted(cnts, key=cv2.contourArea)[-1]
                x, y, w, h = cv2.boundingRect(cnt)  ## (4) Crop and save it

                higher = max(w, h)
                lower = min(w, h)

                diff = (lower / higher) * 100
                if diff > 30:
                    dst = img[y:y + h, x:x + w]
                    return dst
                else:
                    return 0
            else:
                return img
        else:
            raise InappropriateArgsError("croping the image (_crop)")


if __name__ == '__main__':
    img = ProcessImage("ignore", path="./../SamplePictures/sudokuNice.jpg")
    img.get_field_matrix()
    img.draw_lines()
    img.show()