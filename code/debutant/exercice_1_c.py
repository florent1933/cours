input_raw_amount = input("Enter an amount: ")

cleaned_amount = input_raw_amount.replace(",", ".").replace(" ", "").replace("€", "")


print(f"Cleaned amount: {cleaned_amount}, float = {float(cleaned_amount) + 1000}")


print("10" > "3")


if 1 < 2:
    print("1 is less than 3")
else:
    print("1 is not less than 3")
