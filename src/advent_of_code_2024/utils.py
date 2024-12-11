from datetime import datetime
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
