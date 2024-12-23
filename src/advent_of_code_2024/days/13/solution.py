import os
import re
from collections import namedtuple

from advent_of_code_2024.utils import print_part, timer


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    expected_part_one = 480
    result = part_one(test, True)
    if expected_part_one is not None:
        assert (
            result == expected_part_one
        ), f"Part 1 test failed: got {result}, expected {expected_part_one}"
    print(result)
    print(part_one(data))

    # Part 2 test
    # test = """"""
    expected_part_two = 875318608908
    result = part_two(test, True)
    if expected_part_two is not None:
        assert (
            result == expected_part_two
        ), f"Part 2 test failed: got {result}, expected {expected_part_two}"
    print(result)
    print(part_two(data))


Coordinate = namedtuple("Coordinate", ["x", "y"])


@timer
def part_one(data: str, test_run: bool = False):
    """
    Slow brute force solution. More mathematical solution implemented in part two.
    """
    print_part(1, test_run)
    A_BUTTON_PRICE = 3
    B_BUTTON_PRICE = 1

    # Store all parsed claw machines
    claw_machines = []

    # Currently processed claw machine
    claw_machine = {}

    for line in data.splitlines():
        if not line:
            if claw_machine:
                claw_machines.append(claw_machine)
                claw_machine = {}
            continue

        item_type, coords = line.split(":")
        item_type = item_type.split()[-1]

        x_match = re.search(r"X[+=](\d+)", coords)
        y_match = re.search(r"Y[+=](\d+)", coords)
        if not x_match or not y_match:
            raise ValueError(f"Could not parse coordinates from: {coords}")

        x_value = int(x_match.group(1))
        y_value = int(y_match.group(1))
        claw_machine[item_type] = Coordinate(x=x_value, y=y_value)

    # Add the last claw machine after finished processing the input
    if claw_machine:
        claw_machines.append(claw_machine)

    tokens = 0
    for machine in claw_machines:
        target_x = machine["Prize"].x
        target_y = machine["Prize"].y

        """
        For each claw machine, we need to find the minimum number of tokens to reach the prize
            a * target_x + b * B.x = target_x
            a * target_y + b * B.y = target_y
        """

        a_move = machine["A"]
        b_move = machine["B"]

        # Learned that I can and should use infinity in cases like this where I look for minimal solution
        min_tokens = float("inf")

        """
        Calculate maximum reasonable bounds based on target coordinates

        This could actually be replaced with max_tries = 100 because the assignments says that each button can be pressed no more than 100 times.
        I missed that part and calculated the max_tries based on the coordinates.
        """
        max_tries = (
            max(
                abs(target_x // min(a_move.x, b_move.x)),
                abs(target_y // min(a_move.y, b_move.y)),
            )
            + 1
        )

        # Try different combinations and find the most efficient one
        for a in range(max_tries):
            for b in range(max_tries):
                x = a * a_move.x + b * b_move.x
                y = a * a_move.y + b * b_move.y

                if x == target_x and y == target_y:
                    cost = a * A_BUTTON_PRICE + b * B_BUTTON_PRICE
                    if cost < min_tokens:
                        min_tokens = cost

        if min_tokens == float("inf"):
            # No solution found
            min_tokens = 0

        tokens += min_tokens

    return tokens


@timer
def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    A_BUTTON_PRICE = 3

    # Store all parsed claw machines
    claw_machines = []

    # Currently processed claw machine
    claw_machine = {}

    for line in data.splitlines():
        if not line:
            if claw_machine:
                claw_machines.append(claw_machine)
                claw_machine = {}
            continue

        item_type, coords = line.split(":")
        item_type = item_type.split()[-1]

        x_match = re.search(r"X[+=](\d+)", coords)
        y_match = re.search(r"Y[+=](\d+)", coords)
        if not x_match or not y_match:
            raise ValueError(f"Could not parse coordinates from: {coords}")

        x_value = int(x_match.group(1))
        y_value = int(y_match.group(1))
        claw_machine[item_type] = Coordinate(x=x_value, y=y_value)

    # Add the last claw machine after finished processing the input
    if claw_machine:
        claw_machines.append(claw_machine)

    tokens = 0
    for machine in claw_machines:
        target_x = machine["Prize"].x + 10000000000000
        target_y = machine["Prize"].y + 10000000000000
        ax = machine["A"].x
        ay = machine["A"].y
        bx = machine["B"].x
        by = machine["B"].y

        """
        For part two we can no longer bruteforce the solution.
        I managed to form the following equations that I know we need to solve in earlier step:
            a * ax + b * bx = target_x
            a * ay + b * by = target_y

        Had to cheat and look up how to solve these equations without bruteforcing.
        After doing so I think I should have been able to come up with it myself but gave up too early
        since it has been a while since I last did math.

            a = (target_x - b * bx) / ax
            a = (target_y - b * by) / ay
            ax * (target_y - b * by)  = ay * (target_x - b * bx)
            ax * target_y - b * ax * by = ay * target_x - b * ay * bx
            ax * target_y - ay * target_x = b * ax * by - b * ay * bx
            ax * target_y  - ay * target_x = b * (ax * by - ay * bx)
            b = (ax * target_y - ay * target_x)/(ax * by - ay * bx)

        """
        b = (ax * target_y - ay * target_x) / (ax * by - ay * bx)
        a = (target_x - b * bx) / ax

        # Check that b and a are integers since we need a whole number solution
        if int(b) == b and int(a) == a:
            tokens += int(b) + A_BUTTON_PRICE * int(a)

    return tokens
