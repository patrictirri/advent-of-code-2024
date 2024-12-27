import time
from datetime import datetime
from functools import wraps
from pathlib import Path


def get_current_day_number():
    return datetime.now().day


def create_day_dir(day_number: int):
    day_dir = Path(__file__).parent / "days" / f"{day_number}"
    day_dir.mkdir(parents=True, exist_ok=True)


def create_solution_file_from_template(day_number: int):
    template_file = Path(__file__).parent / "days" / "template.py"
    solution_file = Path(__file__).parent / "days" / f"{day_number}" / "solution.py"
    solution_file.write_text(template_file.read_text())


def create_input_file(day_number: int):
    input_file = Path(__file__).parent / "days" / f"{day_number}" / "input.txt"
    input_file.touch()


def get_rows(data: str):
    return data.strip().split("\n")


def create_grid(rows: list[str]):
    grid = {}
    grid_height = len(rows)
    grid_width = len(rows[0]) if rows else 0

    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            grid[(x, y)] = (cell, (x, y))

    grid["height"] = grid_height
    grid["width"] = grid_width
    return grid


def print_part(part: int, test_run: bool = False):
    print()
    test = " (test)" if test_run else ""
    string = f"--- Part {part}{test} ---"
    print(string)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {(end_time - start_time)*1000:.2f} ms")
        return result

    return wrapper
