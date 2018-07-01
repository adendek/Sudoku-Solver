class Validator:
    @staticmethod
    def is_type(value, value_type):
        """
        Check if value is certain type
        :param value: It can be list or a single value of anything
        :param value_type: For which python type are we testing value (str, int, float, list...)
        :return: True if value is that type, False if not
        """
        if isinstance(value, list):
            for val in value:
                if not isinstance(val, value_type):
                    return False
            return True
        return isinstance(value, value_type)

    @staticmethod
    def is_number(value):
        """
        Check if a value is a number (int or float)
        :param value: It can be list or a single value of anything
        :return: True if value is a number, False if not
        """
        if isinstance(value, list):
            for val in value:
                if not (isinstance(val, int) or isinstance(val, float)):
                    return False
            return True
        return isinstance(value, int) or isinstance(value, float)

    @staticmethod
    def is_positive_number(value):
        """
        Check if a value is a positive number (int or float)
        :param value: It can be list or a single value of anything
        :return: True if value is a number, False if not
        """
        if Validator.is_number(value):
            if isinstance(value, list):
                for val in value:
                    if val < 0:
                        return False
                return True
            else:
                return value >= 0
        return False

    @staticmethod
    def is_function(value):
        """
        Check if value is a function
        :param value: It can be list or a single value of anything
        :return: True if value is that function, False if not
        """
        if isinstance(value, list):
            for val in value:
                if not callable(val):
                    return False
            return True
        return callable(value)

    @staticmethod
    def is_9x9_integers_field(value):
        if len(value) == 9 and type(value) == list:
            for row in value:
                if len(row) == 9 and type(value) == list:
                    for column in row:
                        if not Validator.is_type(column, int) or not 0 <= column <= 9:
                            return False
                else:
                    return False
            return True
        return False
