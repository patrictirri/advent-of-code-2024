import os

from advent_of_code_2024.utils import get_rows, print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


def create_grid(rows: list[str]):
    grid = {}
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            grid[(x, y)] = cell
    return grid


def check_direction_part_one(grid: dict, index: tuple[int, int], direction: str):
    sx, sy = index
    directions = {
        "nw": (-1, -1),
        "n": (0, -1),
        "ne": (1, -1),
        "e": (1, 0),
        "se": (1, 1),
        "s": (0, 1),
        "sw": (-1, 1),
        "w": (-1, 0),
    }
    letters = ("M", "A", "S")

    for i in range(1, 4):
        new_index = (
            sx + directions[direction][0] * i,
            sy + directions[direction][1] * i,
        )
        if grid.get(new_index) != letters[i - 1]:
            return 0
    return 1


def find_words(grid: dict, index: tuple[int, int]):
    letter = grid.get(index)
    words = 0

    if letter != "X":
        return words

    for direction in ["nw", "n", "ne", "e", "se", "s", "sw", "w"]:
        words += check_direction_part_one(grid, index, direction)

    return words


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)
    words = 0

    for index in grid:
        words += find_words(grid, index)

    return words


def is_xmas(grid: dict, index: tuple[int, int]):
    sx, sy = index

    top_left = grid.get((sx - 1, sy - 1))
    bottom_right = grid.get((sx + 1, sy + 1))

    bottom_left = grid.get((sx + 1, sy - 1))
    top_right = grid.get((sx - 1, sy + 1))

    downwards_mas = (top_left == "S" and bottom_right == "M") or (
        top_left == "M" and bottom_right == "S"
    )
    upwards_mas = (bottom_left == "S" and top_right == "M") or (
        bottom_left == "M" and top_right == "S"
    )

    if downwards_mas and upwards_mas:
        return 1
    else:
        return 0


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)

    x_mas_count = 0

    for index in grid:
        if grid.get(index) == "A":
            x_mas_count += is_xmas(grid, index)

    return x_mas_count
