from string import digits, ascii_uppercase


class PasswordHasher(object):
    def __init__(self):
        pass

    @classmethod
    def __array_to_number(cls, array, multiplier=None, base=None):
        if multiplier is None:
            if base is None:
                return 0
            else:
                multiplier = [base ** (len(array) - i - 1)
                              for i in range(len(array))]
        number = 0
        for i in range(len(array)):
            try:
                number += array[i] * multiplier[i]
            except ValueError:
                number += ord(array[i]) * multiplier[i]
        return number

    # source: https://bit.ly/2qvGa7i
    @classmethod
    def __primary_string(cls, number, base=36):
        symbols = digits + ascii_uppercase
        if number < base:
            return symbols[number]
        else:
            return cls.__primary_string(number // base) + symbols[number % base]

    @classmethod
    def password_hashing(cls, password):
        length = len(password)
        ascii_codes = [ord(char) for char in password]
        multiplier = [((i ** 4) + ((length - i) * 11)) for i in range(length)]
        original_sum = cls.__array_to_number(ascii_codes, multiplier=multiplier)
        number_in_interval = original_sum % 1679616  # 1679616 = 36 ** 4
        primary = cls.__primary_string(number_in_interval)
        return ('0' * (4 - len(primary))) + primary
