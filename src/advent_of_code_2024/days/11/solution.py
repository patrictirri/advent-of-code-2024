import os
from functools import cache

from advent_of_code_2024.utils import print_part, timer


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """125 17"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


@timer
def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    stones = [int(stone) for stone in data.split(" ")]
    blinks = 0

    while blinks <= 24:
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
                continue

            digit_count = len(str(stone))

            if digit_count % 2 == 0:
                half_length = digit_count // 2
                divisor = 10**half_length
                stone_1 = stone // divisor
                stone_2 = stone % divisor
                new_stones.append(stone_1)
                new_stones.append(stone_2)
                continue

            new_stones.append(stone * 2024)

        stones = new_stones
        blinks += 1

    return len(stones)


@cache
def blink(stone, current=0, max=25):
    """
    Process the stone through the blinks recursively.

    By using a cache, we can memoize the results of the blinks and avoid recalculating them because
    stones with the same value will always turn into the same number of stones after the same number of blinks.
    """
    if current == max:
        return 1

    if stone == 0:
        return blink(1, current + 1, max)

    digit_count = len(str(stone))

    if digit_count % 2 == 0:
        half_length = digit_count // 2
        divisor = 10**half_length
        stone_1 = stone // divisor
        stone_2 = stone % divisor
        return blink(stone_1, current + 1, max) + blink(stone_2, current + 1, max)

    return blink(stone * 2024, current + 1, max)


@timer
def part_two(data: str, test_run: bool = False):
    """
    Part 2 is the same as part 1, but with 75 blinks instead of 24 we can no longer
    process the stones in a reasonable time with brute force.

    Actually, the order of the stones do not matter and we can just follow to how many stones each starting stone
    turns into after 75 blinks and then sum them up.

    This solution ends up being way faster for 75 iterations than the brute force solution for 25 iterations.
    """
    print_part(2, test_run)

    stones = [int(stone) for stone in data.split(" ")]

    stone_count = 0
    for stone in stones:
        stone_count += blink(stone, max=75)
    return stone_count
