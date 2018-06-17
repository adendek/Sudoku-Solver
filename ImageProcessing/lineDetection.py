import cv2
import numpy as np
import operator
from ImageProcessing.line import Line
from ImageProcessing.line import Orientation
from ImageProcessing.numberSquare import NumberSquare
from MachineLearning.skLearn import classify, setup_classifier


class Image:
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path)
        self.height, self.width, self.channels = self.img.shape
        self.grid_lines = self._get_main_lines()
        self.squares = self._get_field_squares()

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
        return squares

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

    def draw_field(self):
        knn = setup_classifier()
        for line in self.squares:
            print("+---+---+---+---+---+---+---+---+---+")
            for i, square in enumerate(line):
                predicted = classify(self.get_image(square), knn)
                if predicted == 0:
                    predicted = " "
                print("|", predicted, "", end="")
                if i == len(line) - 1:
                    print("|")

    def show(self):
        cv2.imshow('Detected Lines.jpg', self.img)
        cv2.waitKey(0)

    def get_image(self, square):
        p1, p2, p3, p4 = square.get_points()
        cut_border = 5
        p1 = (p1[0] + cut_border+3, p1[1] + cut_border)
        p4 = (p4[0] - cut_border, p4[1] - cut_border)
        pts = np.array([[p1[0], p1[1]], [p4[0], p4[1]]])
        r = cv2.boundingRect(pts)
        #cv2.imshow(str(square), self.img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]])
        return self.img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]


if __name__ == '__main__':
    img = Image("sudoku.jpg")
    img.draw_lines()
    img.draw_field()
    img.show()
