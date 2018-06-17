from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError, AddingPointError


class NumberSquare:
    def __init__(self, x, y, tl_point=None):
        if Validator.is_positive_number([x, y]) and Validator.is_type([x, y], int) and x < 9 and y < 9 and \
                (tl_point is None or (Validator.is_type(tl_point, tuple) and
                            Validator.is_positive_number([tl_point[0], tl_point[1]]))):
            self.x_position = x
            self.y_position = y
            self.tl_point = tl_point  # top left point (x, y)
            self.tr_point = None  # top right point (x, y)
            self.bl_point = None  # bottom left point (x, y)
            self.br_point = None  # bottom right point (x, y)
        else:
            raise InappropriateArgsError("creating a NumberSquare!")

    def get_points(self):
        return self.tl_point, self.tr_point, self.bl_point, self.br_point

    def add_point(self, x, y):
        if Validator.is_positive_number([x, y]):
            if self.tl_point is None:
                self.tl_point = (x, y)
            elif self.tr_point is None:
                self.tr_point = (x, y)
            elif self.bl_point is None:
                self.bl_point = (x, y)
            elif self.br_point is None:
                self.br_point = (x, y)
            else:
                raise AddingPointError()
            return x, y
        else:
            raise InappropriateArgsError("adding a point!")
