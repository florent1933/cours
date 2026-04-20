import csv
from pprint import pprint

with open("orders.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    orders = list(reader)

print("Orders:", orders)
pprint(orders)


orders_aggregated = []
for order in orders:
    orders_aggregated.append(
        {
            **order,
            "is_valid_email": True,
        }
    )

print("Orders aggregated:")
pprint(orders_aggregated)


with open("orders_aggregated.csv", "w", encoding="utf-8") as file:
    fieldnames = ["email", "is_valid_email", "montant"]
    writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(orders_aggregated)


dictionnary = {"a": 1, "b": 2, "c": 3}
print(dictionnary.keys())
print(dictionnary.values())

print(dictionnary.items())


for index, order in enumerate(orders):
    print(f"Order {index}: {order}")
