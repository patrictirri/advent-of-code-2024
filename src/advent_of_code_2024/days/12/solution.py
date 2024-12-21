import os
from collections import namedtuple
from typing import Dict, Set, Tuple

from advent_of_code_2024.utils import print_part, timer


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    # print(part_two(test, True))
    # print(part_two(data))


Coordinate = namedtuple("Coordinate", ["x", "y"])
Grid = Dict[Coordinate, str]


def create_grid(rows: list[str]) -> Grid:
    grid = {}
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            grid[Coordinate(x, y)] = cell
    return grid


def get_connected_areas(
    coordinate: Coordinate,
) -> tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
    return (
        Coordinate(coordinate.x + 1, coordinate.y),
        Coordinate(coordinate.x - 1, coordinate.y),
        Coordinate(coordinate.x, coordinate.y + 1),
        Coordinate(coordinate.x, coordinate.y - 1),
    )


def find_region(
    coordinate: Coordinate, grid: Grid, visited: Set[Coordinate]
) -> Tuple[Set[Coordinate], int]:
    """Returns both the region and its perimeter in a single pass"""
    visited.add(coordinate)
    perimeter = 0
    current_value = grid[coordinate]

    for area in get_connected_areas(coordinate):
        area_value = grid.get(area)
        if area_value != current_value:
            perimeter += 1
        elif area not in visited:
            sub_region, sub_perimeter = find_region(area, grid, visited)
            perimeter += sub_perimeter

    return visited, perimeter


def find_regions(grid: Grid) -> list[Tuple[Set[Coordinate], int]]:
    regions = []
    processed = set()

    for coordinate in grid:
        if coordinate in processed:
            continue
        region, perimeter = find_region(coordinate, grid, set())
        processed.update(region)
        regions.append((region, perimeter))

    return regions


@timer
def part_one(data: str, test_run: bool = False) -> int:
    print_part(1, test_run)
    grid = create_grid(data.split("\n"))
    regions = find_regions(grid)

    return sum(len(region) * perimeter for region, perimeter in regions)


@timer
def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    pass
