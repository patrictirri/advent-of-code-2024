import os

from advent_of_code_2024.utils import create_grid, get_rows, print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)
    directions = {
        "N": (-1, 0),
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
    }

    trailheads = []
    for pos, value in grid.items():
        if isinstance(pos, tuple):
            elevation, _ = value
            if int(elevation) == 0:
                trailheads.append(pos)

    total_score = 0
    for trailhead in trailheads:
        queue = [(trailhead, {trailhead})]  # (current_pos, visited_positions)
        routes = set()

        while queue:
            current_pos, visited = queue.pop(0)
            current_elevation, _ = grid[current_pos]
            current_elevation = int(current_elevation)

            for direction in directions:
                new_pos = (
                    current_pos[0] + directions[direction][0],
                    current_pos[1] + directions[direction][1],
                )

                if new_pos not in grid or new_pos in visited:
                    continue

                new_elevation, _ = grid[new_pos]
                new_elevation = int(new_elevation)

                if new_elevation != current_elevation + 1:
                    continue

                new_visited = visited | {new_pos}

                if new_elevation == 9:
                    # Store unique endpoints for trailhead
                    routes.add(new_pos)
                else:
                    queue.append((new_pos, new_visited))

        score = len(routes)
        total_score += score

    return total_score


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    rows = get_rows(data)
    grid = create_grid(rows)
    directions = {
        "N": (-1, 0),
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
    }

    trailheads = []
    for pos, value in grid.items():
        if isinstance(pos, tuple):
            elevation, _ = value
            if int(elevation) == 0:
                trailheads.append(pos)

    total_score = 0
    for trailhead in trailheads:
        queue = [(trailhead, [trailhead])]  # (current_pos, path)
        routes = set()

        while queue:
            current_pos, current_path = queue.pop(0)
            current_elevation, _ = grid[current_pos]
            current_elevation = int(current_elevation)

            for direction in directions:
                new_pos = (
                    current_pos[0] + directions[direction][0],
                    current_pos[1] + directions[direction][1],
                )

                if new_pos not in grid or new_pos in current_path:
                    continue

                new_elevation, _ = grid[new_pos]
                new_elevation = int(new_elevation)

                if new_elevation != current_elevation + 1:
                    continue

                new_path = current_path + [new_pos]

                if new_elevation == 9:
                    # Store the entire path as a tuple to count unique routes
                    routes.add(tuple(new_path))
                else:
                    queue.append((new_pos, new_path))

        score = len(routes)
        total_score += score

    return total_score
