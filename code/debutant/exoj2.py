from pprint import pprint
from code.debutant.emails_utils import clean_email, is_valid_email, get_email_domain

orders = [
    {"email": "alice@acme.com", "montant": "1200,50 €"},
    {"email": "bob@example.fr", "montant": "980.00"},
    {"email": "bob@example.fr", "montant": "1,980.00 $"},
    {"email": "bobexample.fr", "montant": "1,980.00 $"},
]


orders_with_safe_amounts = [
    {"email": "alice@acme.com", "montant": 1200.50},
    {"email": "bob@example.fr", "montant": 980.00},
    {"email": "bob@example.fr", "montant": 1980.00},
    {"email": "bobexample.fr", "montant": 1980.00},
]


def get_float_from_string(amount_str: str) -> float:
    if "$" in amount_str:
        amount_str = amount_str.replace(",", "")

    cleaned_amount = (
        amount_str.replace(",", ".").replace(" ", "").replace("€", "").replace("$", "")
    )

    return float(cleaned_amount)


# for loop
def get_sum():
    total = 0.0

    for row in orders:
        print(row["email"], row["montant"])
        montant_cleaned = get_float_from_string(row["montant"])
        total = total + montant_cleaned

    print(total)


# list de compréhension
def get_sum_with_comprehension_list():
    total = list(order["montant"] for order in orders_with_safe_amounts)
    print("total", total)


# f(x) = x + 1
def get_amount(order):
    return order["montant"]


# with "map"
def get_sum_with_map():
    total = sum(map(get_amount, orders_with_safe_amounts))
    print("total", total)


# filter only $
def get_sum_with_filter():
    total = sum(
        map(
            lambda order: get_float_from_string(order["montant"]),
            filter(lambda order: "$" in order["montant"], orders),
        )
    )
    print("total", total)


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


# orders_amounts = [get_float_from_string(order["montant"]) for order in orders]


orders_transformed = []
for order in orders:
    amount = get_float_from_string(order["montant"])

    valid_email = is_valid_email(clean_email(order["email"]))

    orders_transformed.append(
        {
            **order,
            "montant_cleaned": amount,
            "is_valid_email": valid_email,
            "email_domain": get_email_domain(order["email"]),
        }
    )

print("Transformed orders:")
pprint(orders_transformed)

orders_with_issues = []
for order in orders_transformed:
    if not order["is_valid_email"]:
        orders_with_issues.append(order)


print("Orders with issues:")
pprint(orders_with_issues)


get_sum_with_comprehension_list()
