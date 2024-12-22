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
    expected_part_one = 480  # Replace with expected test result
    result = part_one(test, True)
    if expected_part_one is not None:
        assert (
            result == expected_part_one
        ), f"Part 1 test failed: got {result}, expected {expected_part_one}"
    print(result)
    print(part_one(data))

    # Part 2 test
    # test = """"""
    # expected_part_two = None  # Replace with expected test result
    # result = part_two(test, True)
    # if expected_part_two is not None:
    #     assert result == expected_part_two, f"Part 2 test failed: got {result}, expected {expected_part_two}"
    # print(result)
    # print(part_two(data))


Coordinate = namedtuple("Coordinate", ["x", "y"])


@timer
def part_one(data: str, test_run: bool = False):
    """
    Slow brute force solution.
    Mathematical solution with Extended Euclidean algorithm/GDC would be faster.
    """
    print_part(1, test_run)
    A_BUTTON_PRICE = 3
    B_BUTTON_PRICE = 1

    # Store all parsed claw machines
    claw_machines = []

    # Currently processed claw machine
    claw_machine = {}

    for line in data.splitlines():
        if not line:  # Empty line indicates new machine
            if claw_machine:  # Only append if we have data
                claw_machines.append(claw_machine)
                claw_machine = {}
            continue

        # Parse line: "Button A: X+94, Y+34" or "Prize: X=8400, Y=5400"
        item_type, coords = line.split(":")
        item_type = item_type.split()[-1]  # Get 'A', 'B', or 'Prize'

        # Extract X and Y values using more precise regex
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

        # For each claw machine, we need to find the minimum number of tokens to reach the prize
        # We can use the following system of equations:
        # a * A.x + b * B.x = target_x
        # a * A.y + b * B.y = target_y
        # We need to find non-negative integers a and b that satisfy these equations

        a_move = machine["A"]
        b_move = machine["B"]

        # Initialize minimum tokens to infinity as we are looking for the minimum value
        # Ensures that first valid solution will be saved as the minimum so far
        min_tokens = float("inf")

        # Calculate maximum reasonable bounds based on target coordinates
        max_tries = (
            max(
                abs(target_x // min(a_move.x, b_move.x)),
                abs(target_y // min(a_move.y, b_move.y)),
            )
            + 1
        )

        # Try different combinations (brute force within reasonable bounds) and find the most efficient one
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
    pass
