import HandyMath

num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

print(f"Midpoint: {HandyMath.midpoint(num1, num2)}")
print(f"Square root of the square of {num1}: {HandyMath.square_root(num1 ** 2)}")
print(f"{num1} raised to the exponent of {num2}: {HandyMath.exponent(num1, num2)}")
print(f"Maximum: {HandyMath.max(num1, num2)}")
print(f"Minimum: {HandyMath.min(num1, num2)}")
