orders = [
    {"email": "alice@acme.com", "montant": "1200,50 €"},
    {"email": "bob@example.fr", "montant": "980.00"},
    {"email": "bob@example.fr", "montant": "1,980.00 $"},
]


def get_float_from_string(amount_str: str) -> float:
    if "$" in amount_str:
        amount_str = amount_str.replace(",", "")

    cleaned_amount = (
        amount_str.replace(",", ".").replace(" ", "").replace("€", "").replace("$", "")
    )

    return float(cleaned_amount)


def get_sum():
    total = 0.0

    for row in orders:
        print(row["email"], row["montant"])
        montant_cleaned = get_float_from_string(row["montant"])
        total = total + montant_cleaned

    print(total)


def test_get_float_from_string():

    # print(get_float_from_string("1200.50"))
    # print(get_float_from_string(" 1 200,50 €"))
    # print(get_float_from_string("1 200,50 $"))

    assert get_float_from_string("1100.50") == 1100.50
    assert get_float_from_string(" 1 200,50 €") == 1200.50
    assert get_float_from_string("1,200,50 $") == 1200.50


def main():
    # test_get_float_from_string()
    # print("All tests passed!")
    get_sum()


# main()


orders_amounts = [get_float_from_string(order["montant"]) for order in orders]


orders_amounts = []
for order in orders:
    amount = get_float_from_string(order["montant"])
    orders_amounts.append(amount)
