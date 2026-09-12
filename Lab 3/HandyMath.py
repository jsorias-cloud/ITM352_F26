def midpoint(num1, num2):
    return (num1 + num2) / 2


def square_root(number):
    return number ** 0.5

def max(num1, num2):
    return num1 if num1 > num2 else num2

def min(num1, num2):
    return num1 if num1 < num2 else num2

'''

exponent, which takes two numbers, a base and an exponent, and returns the base raised to the power of the exponent. Code here:

'''

def exponent(base, exp):
    return base ** exp


def celsius_to_fahrenheit(temperature):
    return temperature * 9 / 5 + 32


def celsius_to_kelvin(temperature):
    return temperature + 273.15


def fahrenheit_to_celsius(temperature):
    return (temperature - 32) * 5 / 9


def fahrenheit_to_kelvin(temperature):
    return (temperature - 32) * 5 / 9 + 273.15


def kelvin_to_celsius(temperature):
    return temperature - 273.15


def kelvin_to_fahrenheit(temperature):
    return (temperature - 273.15) * 9 / 5 + 32


def convert_temperature(temperature, conversion_function):
    return conversion_function(temperature)


def describe_function(func):
    if func == midpoint:
        return "This function calculates the midpoint between two numbers."
    elif func == square_root:
        return "This function calculates the square root of a number."
    elif func == max:
        return "This function returns the maximum of two numbers."
    elif func == min:
        return "This function returns the minimum of two numbers."
    elif func == exponent:
        return "This function raises a base number to the power of an exponent."
    else:
        return "Function not recognized."