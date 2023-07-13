from Bot import Constant

from calendar import isleap
import secrets
from random import randint


def GetRandomMail():
    return Constant.mail_list[-1]


def GetVerificationCodeAuto() -> str:
    return "123456"


def GetRandomName(gender: str) -> str:
    if gender.lower() == "m":
        f_name = Constant.first_names_m[randint(0, len(Constant.first_names_m) - 1)]
    else:
        f_name = Constant.first_names_f[randint(0, len(Constant.first_names_f) - 1)]
    l_name = Constant.last_names[randint(0, len(Constant.last_names) - 1)]
    return f"{f_name} {l_name}"


def GetRandomDOB() -> str:
    day = randint(1, 31)
    month = randint(1, 12)
    year = randint(1950, 2000)
    if CheckDate(day, month, year):
        return f"{day}/{month}/{year}"
    else:
        GetRandomDOB()


def GetRandomPassword() -> str:
    password = ''
    for i in range(10):
        password += ''.join(secrets.choice(Constant.password_alphabets))
    return password


def GetRandomUsername(name: str) -> str:
    digit = randint(0, 1000)
    return name[0].upper() + "_" + name.split()[1] + str(digit)


def CheckDate(day: int, month: int, year: int) -> bool:
    if month in [4, 6, 9, 11] and day <= 30:
        return True
    elif month in [1, 3, 5, 7, 8, 10, 12] and day <= 31:
        return True
    elif isleap(year) and month == 2 and day <= 29:
        return True
    elif month == 2 and day <= 28:
        return True
    else:
        return False
