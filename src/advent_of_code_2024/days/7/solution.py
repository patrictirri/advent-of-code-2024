import os

from advent_of_code_2024.utils import get_rows, print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


def try_combinations(numbers, operators, target, current_value=None, ops=None, index=1):
    if current_value is None:
        current_value = numbers[0]
    if ops is None:
        ops = []

    if index == len(numbers):
        return ops if current_value == target else None

    for op_symbol, op_func in operators.items():
        new_value = op_func(current_value, numbers[index])
        result = try_combinations(
            numbers, operators, target, new_value, ops + [op_symbol], index + 1
        )
        if result is not None:
            return result

    return None


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    operators = {
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
    }
    total_calibration_result = 0
    for row in rows:
        test_value, numbers = row.split(":")
        numbers = [int(number) for number in numbers.split()]
        test_value = int(test_value)

        result = try_combinations(numbers, operators, test_value)
        if result:
            total_calibration_result += test_value
    return total_calibration_result


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    rows = get_rows(data)
    operators = {
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
        "||": lambda x, y: int(str(x) + str(y)),
    }
    total_calibration_result = 0
    for row in rows:
        test_value, numbers = row.split(":")
        numbers = [int(number) for number in numbers.split()]
        test_value = int(test_value)

        result = try_combinations(numbers, operators, test_value)
        if result:
            total_calibration_result += test_value
    return total_calibration_result
