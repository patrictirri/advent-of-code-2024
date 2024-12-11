import argparse
import importlib
import sys
from typing import Optional


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run solution for specific day")
    parser.add_argument("day", type=int, help="Day number (1-25)")

    args = parser.parse_args(argv)

    # Validate day is within Advent of Code range
    if not 1 <= args.day <= 25:
        print(f"Error: Day must be between 1 and 25, got {args.day}")
        return 1

    # Here you can add logic to run the specific day's solution
    print(f"Running solution for day {args.day}")
    try:
        # Import the solution module for the specified day
        solution_module = importlib.import_module(
            f"advent_of_code_2024.days.{args.day}.solution"
        )

        # Run the solution's main function
        solution_module.main()
        return 0
    except ImportError:
        print(f"Error: No solution found for day {args.day}")
        return 1
    except Exception as e:
        print(f"Error running solution for day {args.day}: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
