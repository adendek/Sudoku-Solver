from enum import Enum


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.slope = self._configure_slope()
        self.orientation = self._configure_orientation()

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
        a = (line.y1 - line.y2)
        b = (line.x2 - line.x1)
        c = (line.x1 * line.y2 - line.x2 * line.y1)
        return a, b, -c

    @staticmethod
    def get_intersection(line1, line2):
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


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1


if __name__ == '__main__':
    Line.get_intersection(Line(0, 20, 11, 3), Line(3, 2, 1, 0))
