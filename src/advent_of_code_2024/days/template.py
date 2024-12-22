import os

from advent_of_code_2024.utils import print_part, timer


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """"""
    expected_part_one = None  # Replace with expected test result
    result = part_one(test, True)
    if expected_part_one is not None:
        assert (
            result == expected_part_one
        ), f"Part 1 test failed: got {result}, expected {expected_part_one}"
    print(result)
    # print(part_one(data))

    # Part 2 test
    # test = """"""
    # expected_part_two = None  # Replace with expected test result
    # result = part_two(test, True)
    # if expected_part_two is not None:
    #     assert result == expected_part_two, f"Part 2 test failed: got {result}, expected {expected_part_two}"
    # print(result)
    # print(part_two(data))


@timer
def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    pass


@timer
def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    pass
