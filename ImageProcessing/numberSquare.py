class NumberSquare:
    def __init__(self, x, y, tl_point=None):
        self.x_position = x
        self.y_position = y
        self.tl_point = tl_point  # top left point (x, y)
        self.tr_point = None  # top right point (x, y)
        self.bl_point = None  # bottom left point (x, y)
        self.br_point = None  # bottom right point (x, y)

    def get_points(self):
        return self.tl_point, self.tr_point, self.bl_point, self.br_point

    def add_point(self, x, y):
        if self.tl_point is None:
            self.tl_point = (x, y)
        elif self.tr_point is None:
            self.tr_point = (x, y)
        elif self.bl_point is None:
            self.bl_point = (x, y)
        elif self.br_point is None:
            self.br_point = (x, y)
        else:
            print("Square already has 4 points!")
        return x, y
