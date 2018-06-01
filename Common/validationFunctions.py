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

