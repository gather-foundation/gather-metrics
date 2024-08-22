# placeholder.py


def add_numbers(a: int, b: int) -> int:
    return a + b


def greet_user(name: int):
    greeting = f"Hello, {name}!"
    print(greeting)


def calculate_area(radius):
    # This function intentionally lacks type hints and contains a linting issue (missing space around operator).
    pi = 3.14159
    return pi * radius * radius


def main():
    # Test add_numbers function
    sum_result = add_numbers(5, 10)
    print(f"Sum: {sum_result}")

    # Test greet_user function
    greet_user("Alice")

    # Test calculate_area function
    area = calculate_area(5)
    print(f"Area: {area}")


if __name__ == "__main__":
    main()
