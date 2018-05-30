import cv2
import numpy as np
import operator
from Picture.line import Line
from Picture.line import Orientation


class Image:
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path)
        self.height, self.width, self.channels = self.img.shape

    def _get_hough_lines(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)  # Convert the img to gray scale
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # Apply edge detection method on the image
        return cv2.HoughLines(edges, 1, np.pi / 180, 170)

    def _get_lines(self):
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

    def line_minimization(self):
        """
        Keeps only the lines that are needed
        :return: new Dictionary with fewer lines
        """
        max_padding = self._get_padding()  # minimum line distance (if lower the line will be thrown away)
        lines = self._get_lines()

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

    def draw_lines(self):
        for orientation, lines in self.line_minimization().items():
            for line in lines:
                cv2.line(self.img, (line.x1, line.y1), (line.x2, line.y2), (0, 255, 0), 2)

    def show(self):
        cv2.imshow('Detected Lines.jpg', self.img)
        cv2.waitKey(0)


if __name__ == '__main__':
    img = Image("sudokufield.jpg")
    img.draw_lines()
    img.show()
