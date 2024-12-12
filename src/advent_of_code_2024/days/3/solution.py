import os
import re

from advent_of_code_2024.utils import print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    test = (
        """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    )

    print(part_two(test, True))
    print(part_two(data))


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)

    total = 0

    multiplications = [
        (int(x), int(y)) for x, y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
    ]

    for a, b in multiplications:
        total += a * b

    return total


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)

    pattern = r"mul\((\d+),(\d+)\)|don\'t\(\)|do\(\)"
    matches = re.finditer(pattern, data)

    results = []
    for match in matches:
        if match.group(0).startswith("mul"):
            x, y = map(int, match.group(1, 2))
            results.append((x, y))
        elif match.group(0) == "don't()":
            results.append(False)
        elif match.group(0) == "do()":
            results.append(True)

    multiply = True
    total = 0

    for result in results:
        if result is False:
            multiply = False
        elif result is True:
            multiply = True
        else:
            a, b = result
            if multiply:
                total += a * b

    return total
