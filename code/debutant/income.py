income = 3000

high_income = income > 5000  # False
good_credit = False
student = False

eligible = (high_income or good_credit) and not student
print(eligible)
