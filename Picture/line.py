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


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1


if __name__ == '__main__':
    Line(0, 20, -11, 3)
