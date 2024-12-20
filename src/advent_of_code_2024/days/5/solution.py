import os

from advent_of_code_2024.utils import get_rows, print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    # print(part_two(test, True))
    # print(part_two(data))


def find_empty_row(rows: list[str]):
    for row in rows:
        if row == "":
            return rows.index(row)


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    empty_row = find_empty_row(rows)

    if not empty_row:
        raise ValueError("No empty row found")

    ordering_rules, updates = rows[:empty_row], rows[empty_row + 1 :]
    ordering_rules = [tuple(map(int, rule.split("|"))) for rule in ordering_rules]
    updates = [list(map(int, update.split(","))) for update in updates]
    correct_updates = []

    for update in updates:
        update_ok = True
        for rule in ordering_rules:
            if rule[0] in update and rule[1] in update:
                try:
                    x_index = update.index(rule[0])
                    y_index = update.index(rule[1])
                    if x_index > y_index:
                        update_ok = False
                        break
                except ValueError:
                    break
        if update_ok:
            correct_updates.append(update)

    return sum(update[len(update) // 2] for update in correct_updates)


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    pass
