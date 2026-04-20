persons = [
    {"name": "Alice", "age": 30, "email": "alice@example.com"},
    {"name": "Bob", "age": 25, "email": "bob@example.com"},
    {"name": "Charlie", "age": 35, "email": "charlie@example.com"},
]


def transform_person(p):
    return {
        **p,
        "name": p["name"].strip().lower().replace(" ", "_"),
    }


persons = map(transform_person, persons)

print(list(persons))
