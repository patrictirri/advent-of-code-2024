import os
from functools import lru_cache

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

    print(part_two(test, True))
    print(part_two(data))


def find_empty_row(rows: list[str]):
    for row in rows:
        if row == "":
            return rows.index(row)


@lru_cache
def check_updates(ordering_rules: tuple[tuple], updates: tuple[tuple]):
    correct_updates = []
    incorrect_updates = []
    for update in updates:
        update_ok = True
        for rule in ordering_rules:
            if rule[0] in update and rule[1] in update:
                x_index = update.index(rule[0])
                y_index = update.index(rule[1])
                if x_index > y_index:
                    update_ok = False
                    break
        if update_ok:
            correct_updates.append(list(update))
        else:
            incorrect_updates.append(list(update))
    return correct_updates, incorrect_updates


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)
    rows = get_rows(data)
    empty_row = find_empty_row(rows)

    if not empty_row:
        raise ValueError("No empty row found")

    ordering_rules = tuple(
        tuple(map(int, rule.split("|")))[:2] for rule in rows[:empty_row]
    )
    updates = tuple(
        tuple(map(int, update.split(","))) for update in rows[empty_row + 1 :]
    )
    correct_updates, _ = check_updates(ordering_rules, updates)

    return sum(update[len(update) // 2] for update in correct_updates)


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)
    rows = get_rows(data)
    empty_row = find_empty_row(rows)

    if not empty_row:
        raise ValueError("No empty row found")

    ordering_rules = tuple(
        tuple(map(int, rule.split("|")))[:2] for rule in rows[:empty_row]
    )
    updates = tuple(
        tuple(map(int, update.split(","))) for update in rows[empty_row + 1 :]
    )
    _, incorrect_updates = check_updates(ordering_rules, updates)

    for incorrect_update in incorrect_updates:
        while True:
            violation_found = False
            for rule in ordering_rules:
                if rule[0] in incorrect_update and rule[1] in incorrect_update:
                    x_index = incorrect_update.index(rule[0])
                    y_index = incorrect_update.index(rule[1])
                    if x_index > y_index:
                        x = incorrect_update.pop(x_index)
                        incorrect_update.insert(y_index, x)
                        violation_found = True
                        break
            if not violation_found:
                break

    return sum(update[len(update) // 2] for update in incorrect_updates)
