list = [1, 2, 3, 4, 5]


list.append(6)
print(list)


list_b = [
    *list,
    7,
]


def add_item_mutation(lists):
    lists.append(1)


var1 = []
add_item_mutation(var1)
print("🤞", var1 == [1])
add_item_mutation(var1)
print("🤞", var1 == [1, 1])


def add_item_pure(lists):
    return [*lists, 1]


def is_even(i):
    return i % 2 == 0


list2 = [8, 9, 10]

print(list)


# f(x) = None
# f(1) = 1
# f(2) = 2
def nothing_append(x: int):
    return x


def to_upper_string(s: str) -> str:
    return s.upper()


def remove_accent(s: str) -> str:
    return s.replace("é", "e").replace("ó", "o")


# f("Rodrigue")= "RODRIGUE"


print("upper string rodrique", to_upper_string("Rodrigue") == "RODRIGUE")
print("remove accent", remove_accent("Rodrigué") == "Rodrigue")
print("remove accent", remove_accent("Ródrigue") == "Rodrigue")


"-".join(["a", "b", "c", "d", "e"])  # "a-b-c-de"
