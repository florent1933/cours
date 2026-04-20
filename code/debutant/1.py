print("Hello, World!Merci. =Merci.")
print(10 * "x")


def f(x):
    return x * 2


print(f(10))

print("This is a test.")
print("Hello" * 10, end="---")


score = 10


clients = ["Alice", "Bob", "Charlie"]

for i, client in enumerate(clients):
    print(f"Hello, {client}, {i}!")


x = {"name": "Alice", "age": 30, "city": "New York"}

print("name", x["name"])


nom: str = "Alice"
age: int | None = 30
is_student: bool = False
