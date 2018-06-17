from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
from enum import Enum


class Line:
    def __init__(self, x1, y1, x2, y2):
        if Validator.is_positive_number([x1, y1, x2, y2]) and not (x1 == x2 and y1 == y2):  # not a line
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.slope = self._configure_slope()
            self.orientation = self._configure_orientation()
        else:
            raise InappropriateArgsError("creating a line")

    def get_orientation(self):
        return self.orientation

    def get_slope(self):
        return self.slope

    def _configure_orientation(self):
        if abs(self.slope) >= 1:
            return Orientation.Vertical
        return Orientation.Horizontal

    def _configure_slope(self):
        up = self.y2 - self.y1
        down = self.x2 - self.x1
        if down == 0:  # line is vertical
            return 100
        return float("%.2f" % (up / down))

    @staticmethod
    def get_coefs(line):
        if Validator.is_type(line, Line):
            a = (line.y1 - line.y2)
            b = (line.x2 - line.x1)
            c = (line.x1 * line.y2 - line.x2 * line.y1)
            return a, b, -c
        else:
            raise InappropriateArgsError("getting coefficients")

    @staticmethod
    def get_intersection(line1, line2):
        if Validator.is_type([line1, line2], Line):
            coefs1 = Line.get_coefs(line1)
            coefs2 = Line.get_coefs(line2)
            d = coefs1[0] * coefs2[1] - coefs1[1] * coefs2[0]
            dx = coefs1[2] * coefs2[1] - coefs1[1] * coefs2[2]
            dy = coefs1[0] * coefs2[2] - coefs1[2] * coefs2[0]
            if d != 0:
                x = dx / d
                y = dy / d
                return round(x), round(y)
            else:
                return False
        else:
            raise InappropriateArgsError("getting intersection points")


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1
