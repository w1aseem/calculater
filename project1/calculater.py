import math


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    else:
        return x / y


def exponent(x, y):
    return x**y


def modulus(x, y):
    return x % y


def floor_divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    else:
        return x // y


# single -input operations


def square_root(x):
    if x < 0:
        return "cannot take square root of negative number"
    else:
        return math.sqrt(x)


def log10(x):
    if x <= 0:
        return "logarithm undefined for non-positive numbers"
    else:
        return math.log10(x)


def natural_log(x):
    if x <= 0:

        return "natural log undefined for non -positive numbers"

    else:
        return math.log(x)


def sine(x):
    return math.sin(math.radians(x))


def cosine(x):
    return math.cos(math.radians(x))


def tangent(x):
    return math.tan(math.radians(x))


def factorial(x):
    if x < 0:
        return "factorial not defined for negative numbers"
    else:
        return math.factorial(x)


def absolute(x):
    return abs(x)


def power_of_ten(x):

    return 10**x


def radians(x):

    return math.radians(x)


def degrees(x):

    return math.degrees(x)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def sinh(x):

    return math.sinh(x)


def cosh(x):
    return math.cosh(x)


def tanh(x):
    return math.tanh(x)


def asin(x):
    if -1 <= x <= 1:
        return math.degrees(math.asin(x))
    else:
        return "involid input for asin"


def acos(x):
    if -1 <= x <= 1:
        return math.degrees(math.acos(x))
    else:
        return "invalid input for acos"


def atan(x):

    return math.degrees(math.atan(x))


# two-iinput operations


def clamp(x, min_value, max_value):

    return max(min(x, max_value), min_value)


def percentage(x, precent):

    return (x * precent) / 100


def gcd(x, y):
    return math.gcd(int(x), int(y))


def lcm(x, y):
    return abs(int(x) * int(y)) // math.gcd(int(x), int(y))


def log_custom(x, base):
    if x <= 0 or base <= 0 or base == 1:

        return "logarithm undefined for non-positive numbers"

    else:
        math.log(x, base)
