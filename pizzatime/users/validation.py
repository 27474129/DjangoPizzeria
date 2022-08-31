import re
from .models import Users


class Validation:
    def __init__(self, firstname, secondname, phone, password, password_repeat):
        self.validation_errors = ""
        self.validation_errors += Validation.validate_names(firstname, "firstname")
        self.validation_errors += Validation.validate_names(secondname, "secondname")
        self.validation_errors += Validation.validate_phone(phone)
        self.validation_errors += Validation.validate_password(password)


        if (password != password_repeat):
            self.validation_errors += "Пароли не совпадают;"



    @staticmethod
    def validate_names(name, var_name):
        errors = ""
        if (len(name) < 3):
            if (var_name == "firstname"):
                errors += "Имя должно состоять минимум из 3х символов;"
            else:
                errors += "Фамилия должна состоять минимум из 3х символов;"

        en_lower_letters = re.findall(r"[a-z]", name)
        en_upper_letters = re.findall(r"[A-Z]", name)
        ru_upper_letters = re.findall(r"[А-Я]", name)
        ru_lower_letters = re.findall(r"[а-я]", name)

        if (
            len(en_lower_letters) + len(en_upper_letters) +
            len(ru_lower_letters) + len(ru_upper_letters) != len(name)
        ):
            if (var_name == "firstname"):
                errors += "Имя должно состоять только из букв;"
            else:
                errors += "Фамилия должна состоять только из букв;"

        return errors


    @staticmethod
    def validate_phone(phone):
        errors = ""
        if (len(phone) != 10):
            errors += "Номер телефона должен содержать ровно 10 цифр (не пишите цифры региона в начале);"

        match = Users.objects.filter(phone=phone)
        if (len(match) != 0):
            errors += "Номер телефона уже занят;"

        return errors


    @staticmethod
    def validate_password(password):
        errors = ""
        if (len(password) < 7):
            errors += "Длина пароля должна быть не менее 7 символов;"

        digits_count = len(re.findall(r"[0-9]", password))
        lower_letters_count = len(re.findall(r"[a-z]", password))
        upper_letters_count = len(re.findall(r"[A-Z]", password))

        if (digits_count < 2):
            errors += "Пароль должен содержать 2 цифры и более;"
        if (lower_letters_count + upper_letters_count < 2):
            errors += "Пароль должен содержать 2 буквы и более;"

        if (lower_letters_count + upper_letters_count + digits_count != len(password)):
            errors += "Пароль может содержать только цифры и буквы разных регистров;"

        return errors
