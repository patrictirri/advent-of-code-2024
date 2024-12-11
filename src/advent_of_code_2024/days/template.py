import os


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


def print_part(part: int, test_run: bool = False):
    string = f"Part {part}"
    if test_run:
        string += " (test)"
    print(string)


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    pass


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    pass
