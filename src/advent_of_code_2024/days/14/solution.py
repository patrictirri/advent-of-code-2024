import os
from dataclasses import dataclass

from advent_of_code_2024.utils import get_rows, print_part, timer


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    expected_part_one = 12
    result = part_one(test, True)
    if expected_part_one is not None:
        assert (
            result == expected_part_one
        ), f"Part 1 test failed: got {result}, expected {expected_part_one}"
    print("Test result:", result)
    print("Result:", part_one(data))

    # Part 2 test
    print("Result:", part_two(data))


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class Velocity:
    x: int
    y: int


@dataclass
class Robot:
    position: Coordinate
    velocity: Velocity


@timer
def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    bathroom_width = 11 if test_run else 101
    bathroom_height = 7 if test_run else 103
    seconds = 100

    robots = []
    quadrants = [0, 0, 0, 0]
    for row in rows:
        pos, vel = row.split()
        pos_x, pos_y = pos.split("=")[1].split(",")
        vel_x, vel_y = vel.split("=")[1].split(",")
        robots.append(
            Robot(
                Coordinate(int(pos_x), int(pos_y)),
                Velocity(int(vel_x), int(vel_y)),
            )
        )

    for robot in robots:
        position = Coordinate(
            (robot.position.x + (robot.velocity.x * seconds)) % bathroom_width,
            (robot.position.y + (robot.velocity.y * seconds)) % bathroom_height,
        )

        left = position.x < bathroom_width // 2
        right = position.x > bathroom_width // 2
        top = position.y < bathroom_height // 2
        bottom = position.y > bathroom_height // 2

        if left and top:
            quadrants[0] += 1
        elif right and top:
            quadrants[1] += 1
        elif left and bottom:
            quadrants[2] += 1
        elif right and bottom:
            quadrants[3] += 1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


@timer
def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    rows = get_rows(data)
    bathroom_width = 101
    bathroom_height = 103

    robots = []
    for row in rows:
        pos, vel = row.split()
        pos_x, pos_y = pos.split("=")[1].split(",")
        vel_x, vel_y = vel.split("=")[1].split(",")
        robots.append(
            Robot(Coordinate(int(pos_x), int(pos_y)), Velocity(int(vel_x), int(vel_y)))
        )

    seconds = 0
    while True:
        seconds += 1
        for robot in robots:
            robot.position = Coordinate(
                (robot.position.x + robot.velocity.x) % bathroom_width,
                (robot.position.y + robot.velocity.y) % bathroom_height,
            )

        if len(set(robot.position for robot in robots)) == len(robots):
            break

    return seconds
