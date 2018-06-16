class InappropriateArgsError(Exception):
    def __init__(self, name):
        super().__init__("Inappropriate arguments when " + name + "!")
