import os

from advent_of_code_2024.utils import create_grid, get_rows, print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


frequencies = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def find_antennas(grid: dict, frequency: str):
    antennas = []
    for key, cell in grid.items():
        if isinstance(key, tuple):
            if cell[0] == frequency:
                antennas.append(key)
    return antennas


def is_point_in_line(point, p1, p2):
    x1, y1 = point[0] - p1[0], point[1] - p1[1]
    x2, y2 = p2[0] - p1[0], p2[1] - p1[1]
    cross_product = x1 * y2 - x2 * y1
    return cross_product == 0


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)

    antinodes = set()
    antenna_dict = {}
    for frequency in frequencies:
        found_antennas = find_antennas(grid, frequency)
        antenna_dict[frequency] = found_antennas

    for frequency, antennas in antenna_dict.items():
        if len(antennas) < 2:
            continue

        for i in range(len(antennas)):
            for j in range(i + 1, len(antennas)):
                antenna_1 = antennas[i]
                antenna_2 = antennas[j]

                dx = antenna_2[0] - antenna_1[0]
                dy = antenna_2[1] - antenna_1[1]

                antinode_1 = (antenna_1[0] + (dx * -1), antenna_1[1] + (dy * -1))
                antinode_2 = (antenna_2[0] + dx, antenna_2[1] + dy)

                for antinode in [antinode_1, antinode_2]:
                    if (
                        0 <= antinode[0] < grid["width"]
                        and 0 <= antinode[1] < grid["height"]
                    ):
                        antinodes.add(antinode)

    return len(antinodes)


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)

    antinodes = set()
    antenna_dict = {}
    for frequency in frequencies:
        antenna_dict[frequency] = find_antennas(grid, frequency)

    for frequency, antennas in antenna_dict.items():
        if len(antennas) < 2:
            continue

        for y in range(grid["height"]):
            for x in range(grid["width"]):
                point = (x, y)

                for i in range(len(antennas)):
                    for j in range(i + 1, len(antennas)):
                        antenna_1 = antennas[i]
                        antenna_2 = antennas[j]

                        if not is_point_in_line(point, antenna_1, antenna_2):
                            continue

                        antinodes.add(point)
                        break

    return len(antinodes)
