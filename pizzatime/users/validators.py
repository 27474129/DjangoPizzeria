import re
from .models import Users



def validate_names(name, var_name, add_error):
    exceptions = []
    if (len(name) < 3):
        if (var_name == "firstname"):
            exceptions.append("Имя должно состоять минимум из 3х символов")
        else:
            exceptions.append("Фамилия должна состоять минимум из 3х символов")

    en_lower_letters = re.findall(r"[a-z]", name)
    en_upper_letters = re.findall(r"[A-Z]", name)
    ru_upper_letters = re.findall(r"[А-Я]", name)
    ru_lower_letters = re.findall(r"[а-я]", name)

    if (
        len(en_lower_letters) + len(en_upper_letters) +
        len(ru_lower_letters) + len(ru_upper_letters) != len(name)
    ):
        if (var_name == "firstname"):
            exceptions.append("Имя должно состоять только из букв")
        else:
            exceptions.append("Фамилия должна состоять только из букв")

    for exception in exceptions:
        if (var_name == "firstname"):
            add_error("firstname", exception)
        else:
            add_error("secondname", exception)



def validate_phone(phone, add_error):
    exceptions = []
    if (len(phone) != 10):
        exceptions.append("Номер телефона должен содержать ровно 10 цифр (не пишите цифры региона в начале)")

    match = Users.objects.filter(phone=phone)
    if (len(match) != 0):
        exceptions.append("Номер телефона уже занят")

    for exception in exceptions:
        add_error("phone", exception)


def validate_password(password, add_error):
    exceptions = []
    if (len(password) < 7):
        exceptions.append("Длина пароля должна быть не менее 7 символов")

    digits_count = len(re.findall(r"[0-9]", password))
    lower_letters_count = len(re.findall(r"[a-z]", password))
    upper_letters_count = len(re.findall(r"[A-Z]", password))

    if (digits_count < 2):
        exceptions.append("Пароль должен содержать 2 цифры и более")
    if (lower_letters_count + upper_letters_count < 2):
        exceptions.append("Пароль должен содержать 2 буквы и более")

    if (lower_letters_count + upper_letters_count + digits_count != len(password)):
        exceptions.append("Пароль может содержать только цифры и буквы разных регистров")


    for exception in exceptions:
        add_error("password", exception)

