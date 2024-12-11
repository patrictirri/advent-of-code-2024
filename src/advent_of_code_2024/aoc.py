import sys

from advent_of_code_2024.utils import (
    create_day_dir,
    create_input_file,
    create_solution_file_from_template,
    get_current_day_number,
)


def main():
    print("Initializing new day")
    day_number = int(sys.argv[1]) if len(sys.argv) > 1 else get_current_day_number()
    create_day_dir(day_number)
    create_solution_file_from_template(day_number)
    create_input_file(day_number)
    print(f"Day {day_number} initialized")


if __name__ == "__main__":
    main()
