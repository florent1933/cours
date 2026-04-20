from cleaners import normalize_amount

print(normalize_amount(" 999€"))

x = range(10)

print("✨", list(x))


def triple(i: int) -> int:
    return i * 3


def is_even(i: int) -> bool:
    return i % 2 == 0


# for loop
listt = []
for i in x:
    if is_even(i):
        listt.append(triple(i))
print(listt)

# with "map"
list_with_map = list(filter(is_even, map(triple, filter(is_even, x))))
print(list_with_map)


# with "list comprehension"
list_with_comprehension = [
    x for x in [triple(i) for i in x if is_even(i)] if is_even(x)
]
print(list_with_comprehension)
