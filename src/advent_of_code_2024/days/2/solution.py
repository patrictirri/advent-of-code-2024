import os

from advent_of_code_2024.utils import get_rows


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

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
    reports = get_rows(data)

    safe_reports = 0

    for report in reports:
        levels = [int(x) for x in report.split(" ")]

        pairs = zip(levels, levels[1:])
        is_ascending = all(a < b and abs(b - a) <= 3 for a, b in pairs)

        pairs = zip(levels, levels[1:])
        is_descending = all(a > b and abs(a - b) <= 3 for a, b in pairs)

        descending_or_ascending = is_ascending or is_descending
        if descending_or_ascending:
            safe_reports += 1

    return safe_reports


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    pass
