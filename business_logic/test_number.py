def getNumber() -> float:
    while True:
        n = input("Enter a number: ")
        try:
            return float(n)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


OPERATORS = ["+", "-", "*", "/"]


def getOperator():
    operator = ""
    while operator not in OPERATORS:
        operator = input("Enter an operator (+ - * / ): ")
    return operator


n1 = getNumber()
n2 = getNumber()

operator = getOperator()

if operator == "+":
    print(n1 + n2)
elif operator == "-":
    print(n1 - n2)
elif operator == "*":
    print(n1 * n2)
elif operator == "/":
    if n2 == 0:
        print("Error: division by zero")
    else:
        print(n1 / n2)
else:
    print("Error: invalid operator")
