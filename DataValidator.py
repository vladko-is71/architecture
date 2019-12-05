from string import digits, ascii_lowercase, ascii_uppercase


class DataValidator:
    def __init__(self):
        pass

    @staticmethod
    def email_validation(email):
        if email.count('@') != 1:
            return False
        index = email.find('@')
        if email[index+1:].count('.') == 0:
            return False
        return True

    @staticmethod
    def password_validation(password):
        if len(password) < 6 or len(password) > 32:
            return False
        possible_chars = ascii_uppercase + ascii_lowercase + digits
        for character in password:
            if character not in possible_chars:
                return False
        return True
