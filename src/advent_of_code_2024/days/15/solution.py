import os
from typing import NamedTuple

from advent_of_code_2024.utils import get_rows, print_part, timer


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

    expected_part_one = 10092
    result = part_one(test, True)
    if expected_part_one is not None:
        assert (
            result == expected_part_one
        ), f"Part 1 test failed: got {result}, expected {expected_part_one}"
    print("Test result:", result)
    print("Result:", part_one(data))

    # Part 2 test
    # test = """"""
    # expected_part_two = None  # Replace with expected test result
    # result = part_two(test, True)
    # if expected_part_two is not None:
    #     assert result == expected_part_two, f"Part 2 test failed: got {result}, expected {expected_part_two}"
    # print("Result:", result)
    # print("Test result:", part_two(data))
    print()


class Objects:
    ROBOT = "@"
    BOX = "O"
    EMPTY = "."
    WALL = "#"


class Position(NamedTuple):
    x: int
    y: int


class Grid:
    def __init__(self, grid_data: str):
        self.grid = self._create_grid(get_rows(grid_data))
        self.robot_position = self._get_robot_position()

    def _create_grid(self, rows: list[str]):
        return {
            Position(x, y): value
            for y, row in enumerate(rows)
            for x, value in enumerate(row)
            if value != " "
        }

    def _get_robot_position(self) -> Position:
        for pos, value in self.grid.items():
            if value == Objects.ROBOT:
                return pos
        raise ValueError("Robot not found in grid")

    def _get_direction(self, direction: str) -> Position:
        DIRECTIONS = {
            ">": Position(1, 0),
            "<": Position(-1, 0),
            "^": Position(0, -1),
            "v": Position(0, 1),
        }
        if direction not in DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")
        return DIRECTIONS[direction]

    def _try_push_boxes(self, start_pos: Position, delta: Position) -> bool:
        boxes = []
        current = start_pos
        while self.grid.get(current) == Objects.BOX:
            boxes.append(current)
            current = Position(current.x + delta.x, current.y + delta.y)

        if self.grid.get(current) == Objects.WALL:
            return False

        for box_pos in boxes[::-1]:
            new_pos = Position(box_pos.x + delta.x, box_pos.y + delta.y)
            self.grid[new_pos] = Objects.BOX
            self.grid[box_pos] = Objects.EMPTY
        return True

    def move(self, direction: str) -> None:
        delta = self._get_direction(direction)
        next_position = Position(
            self.robot_position.x + delta.x, self.robot_position.y + delta.y
        )
        next_object = self.grid.get(next_position)

        if next_object == Objects.WALL:
            return
        if next_object == Objects.EMPTY:
            self.robot_position = next_position
            return
        if next_object == Objects.BOX:
            if self._try_push_boxes(next_position, delta):
                self.robot_position = next_position

    def calculate_gps(self) -> int:
        return sum(
            pos.y * 100 + pos.x
            for pos, value in self.grid.items()
            if value == Objects.BOX
        )


@timer
def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    grid, movements = data.split("\n\n")
    grid = Grid(grid)
    movements = "".join(movements.split("\n"))

    for direction in movements:
        grid.move(direction)

    return grid.calculate_gps()


@timer
def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    pass
