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

    print(part_two(test, True))
    print(part_two(data))


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
    """Returns the four connected areas for a given coordinate"""
    return (
        Coordinate(coordinate.x + 1, coordinate.y),
        Coordinate(coordinate.x - 1, coordinate.y),
        Coordinate(coordinate.x, coordinate.y + 1),
        Coordinate(coordinate.x, coordinate.y - 1),
    )


def find_region_and_perimeter(
    coordinate: Coordinate, grid: Grid, visited: set[Coordinate]
) -> Tuple[Set[Coordinate], int]:
    """Returns region and its perimeter"""
    visited.add(coordinate)
    perimeter = 0
    current_value = grid[coordinate]

    for area in get_connected_areas(coordinate):
        area_value = grid.get(area)
        if area_value != current_value:
            perimeter += 1
        elif area not in visited:
            _, sub_perimeter = find_region_and_perimeter(area, grid, visited)
            perimeter += sub_perimeter

    return visited, perimeter


def find_regions(grid: Grid) -> list[tuple[set[Coordinate], int]]:
    """
    Returns a list of regions and their perimeters.
    Uses a flood fill algorithm to find a region (set of coordinates) that connected areas of same characters.
    """
    regions = []
    processed = set()

    for coordinate in grid:
        if coordinate in processed:
            continue
        region, perimeter = find_region_and_perimeter(coordinate, grid, set())
        processed.update(region)
        regions.append((region, perimeter))

    return regions


@timer
def part_one(data: str, test_run: bool = False) -> int:
    print_part(1, test_run)
    grid = create_grid(data.split("\n"))
    regions = find_regions(grid)

    return sum(len(region) * perimeter for region, perimeter in regions)


def are_both_in_region(pos1, pos2, region):
    return pos1 in region and pos2 in region


def are_both_outside_region(pos1, pos2, region):
    return not (pos1 in region or pos2 in region)


def count_region_corners(pos, region, grid, other_regions, check_inside=False):
    # Define the four possible corner configurations around a position
    # Each corner is defined by two adjacent positions (diagonal corners)
    adjacent = {
        "left_up": (Coordinate(pos.x - 1, pos.y), Coordinate(pos.x, pos.y - 1)),
        "left_down": (Coordinate(pos.x - 1, pos.y), Coordinate(pos.x, pos.y + 1)),
        "right_up": (Coordinate(pos.x + 1, pos.y), Coordinate(pos.x, pos.y - 1)),
        "right_down": (Coordinate(pos.x + 1, pos.y), Coordinate(pos.x, pos.y + 1)),
    }

    if check_inside:
        # When checking inside corners, count how many pairs of adjacent positions
        # are both part of the region
        return sum(
            are_both_in_region(pos1, pos2, region) for pos1, pos2 in adjacent.values()
        )

    # When checking outside corners, count valid corners where both positions are
    # outside the region and form a valid corner configuration
    return sum(
        are_both_outside_region(pos1, pos2, region)
        and is_valid_corner(pos1, pos2, other_regions, grid)
        for pos1, pos2 in adjacent.values()
    )


def calculate_region_price(region):
    # Find the bounding box of the region
    bounds = {
        "x": (min(coord.x for coord in region), max(coord.x for coord in region)),
        "y": (min(coord.y for coord in region), max(coord.y for coord in region)),
    }

    # Create a simplified grid where the region is marked with 'x' and everything else with '.'
    grid = {
        Coordinate(x, y): "x" if Coordinate(x, y) in region else "."
        for y in range(bounds["y"][0], bounds["y"][1] + 1)
        for x in range(bounds["x"][0], bounds["x"][1] + 1)
    }

    # Find all other regions in the grid (holes/gaps in the main region)
    other_regions = [
        sub_region[0] for sub_region in find_regions(grid) if sub_region[0] != region
    ]

    # Calculate total price by:
    # 1. Summing outside corners for each position in the region
    # 2. Adding inside corners from positions in other regions (holes)
    return sum(
        count_region_corners(pos, region, grid, other_regions) for pos in region
    ) + sum(
        count_region_corners(pos, region, grid, [], check_inside=True)
        for other in other_regions
        for pos in other
    )


def is_valid_corner(pos1, pos2, other_regions, grid):
    # Early return if positions are not in grid
    if not (grid.get(pos1) and grid.get(pos2)):
        return True

    return not any((pos1 in other) != (pos2 in other) for other in other_regions)


@timer
def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    grid = create_grid(data.split("\n"))
    regions = find_regions(grid)

    price = 0
    for region, _ in regions:
        sides = calculate_region_price(region)
        price += sides * len(region)

    return price
