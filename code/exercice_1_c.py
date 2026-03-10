input_raw_amount = input("Enter an amount: ")

cleaned_amount = input_raw_amount.replace(",", ".").replace(" ", "").replace("€", "")


print(f"Cleaned amount: {cleaned_amount}, float = {float(cleaned_amount) + 1000}")
