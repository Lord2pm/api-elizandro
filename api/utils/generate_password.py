from random import choice, randrange
from string import ascii_letters


def generate_password():
    password = ""
    for i in range(12):
        if i % 2 == 0:
            password += choice(ascii_letters)
        else:
            password += str(randrange(0, 9))
    return password
