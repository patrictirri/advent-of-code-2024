import os

from advent_of_code_2024.utils import get_rows, print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


def is_obstacle(obstacles: list[tuple[int, int]], next_cell: tuple[int, int]):
    return next_cell in obstacles


def find_obstacles(grid: dict):
    obstacles = []
    for key, cell in grid.items():
        if isinstance(key, tuple):
            if cell[0] == "#":
                obstacles.append(key)
    return obstacles


def is_off_the_grid(grid: dict, next_cell: tuple[int, int]):
    return (
        next_cell[0] < 0
        or next_cell[0] >= grid["width"]
        or next_cell[1] < 0
        or next_cell[1] >= grid["height"]
    )


def move_guard(
    grid: dict,
    guard_position: tuple[int, int],
    direction: str,
    visited: set[tuple[int, int]],
    guard_in_laboratory: bool,
    obstacles: list[tuple[int, int]],
):
    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }

    turn_right = {"N": "E", "E": "S", "S": "W", "W": "N"}

    next_cell = (
        guard_position[0] + directions[direction][0],
        guard_position[1] + directions[direction][1],
    )

    if is_obstacle(obstacles, next_cell):
        direction = turn_right[direction]
        return guard_position, direction, visited, guard_in_laboratory, obstacles

    if is_off_the_grid(grid, next_cell):
        guard_in_laboratory = False
        return guard_position, direction, visited, guard_in_laboratory, obstacles

    visited.add(next_cell)
    return next_cell, direction, visited, guard_in_laboratory, obstacles


def create_grid(rows: list[str]):
    grid = {}
    grid_height = len(rows)
    grid_width = len(rows[0]) if rows else 0

    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            grid[(y, x)] = (cell, (y, x))

    grid["height"] = grid_height
    grid["width"] = grid_width
    return grid


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)
    guard_position = next(
        (pos for pos in grid.keys() if isinstance(pos, tuple) and grid[pos][0] == "^")
    )
    current_direction = "N"
    guard_in_laboratory = True
    visited = {guard_position}
    obstacles = find_obstacles(grid)

    while guard_in_laboratory:
        guard_position, current_direction, visited, guard_in_laboratory, obstacles = (
            move_guard(
                grid,
                guard_position,
                current_direction,
                visited,
                guard_in_laboratory,
                obstacles,
            )
        )

    return len(visited)


def part_two(data: str, test_run: bool = False):
    """
    Takes minutes to run and is really hacky :D please optimize and implement proper solution
    """
    print_part(2, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)
    guard_position = next(
        (pos for pos in grid.keys() if isinstance(pos, tuple) and grid[pos][0] == "^")
    )
    current_direction = "N"
    possible_traps = []

    empty_spaces = [
        pos for pos in grid.keys() if isinstance(pos, tuple) and grid[pos][0] == "."
    ]

    for position in empty_spaces:
        obstacles = find_obstacles(grid) + [position]
        guard_pos = guard_position
        direction = current_direction
        visited = {guard_position}
        guard_in_laboratory = True

        steps = 0
        max_steps = len(empty_spaces) * 4

        while guard_in_laboratory and steps < max_steps:
            guard_pos, direction, visited, guard_in_laboratory, _ = move_guard(
                grid, guard_pos, direction, visited, guard_in_laboratory, obstacles
            )

            steps += 1

            if not guard_in_laboratory:
                break

        if guard_in_laboratory and steps >= max_steps:
            possible_traps.append((position, len(visited)))

    return len(possible_traps)
