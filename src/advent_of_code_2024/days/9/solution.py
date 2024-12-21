import os
from copy import deepcopy

from advent_of_code_2024.utils import print_part


def main():
    INPUT = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(INPUT) as f:
        data = f.read()

    test = """2333133121414131402"""

    print(part_one(test, True))
    print(part_one(data))

    # Part 2 test
    # test = """"""

    print(part_two(test, True))
    print(part_two(data))


def find_first_empty_space(formatted_data: list):
    for index, item in enumerate(formatted_data):
        if item is None:
            return index
    return None


def part_one(data: str, test_run: bool = False):
    print_part(1, test_run)

    formatted_data = []
    id = 0
    for index, number in enumerate(data):
        if index % 2 != 0:
            formatted_data.extend([None] * int(number))
        else:
            formatted_data.extend([id] * int(number))
            id += 1

    ordered_files = deepcopy(formatted_data)

    for index in range(len(formatted_data) - 1, -1, -1):
        item = formatted_data[index]
        if item is not None:
            empty_space_index = find_first_empty_space(ordered_files[:index])
            if empty_space_index is not None:
                ordered_files[empty_space_index] = item
                ordered_files[index] = None

    checksum = 0

    for index, item in enumerate(ordered_files):
        if item is not None:
            checksum += index * item
        else:
            # We've reached the end of the valid files
            break

    return checksum


def part_two(data: str, test_run: bool = False):
    print_part(2, test_run)

    formatted_data = []
    id = 0
    for index, number in enumerate(data):
        if index % 2 != 0:
            formatted_data.extend([None] * int(number))
        else:
            formatted_data.extend([id] * int(number))
            id += 1

    ordered_files = deepcopy(formatted_data)

    current_file = []
    current_item = None
    for index in range(len(formatted_data) - 1, -1, -1):
        item = formatted_data[index]

        if item != current_item or item is None:
            if current_file:
                file_length = len(current_file)
                for start_idx in range(index + 1):
                    if all(
                        ordered_files[i] is None
                        for i in range(
                            start_idx, min(start_idx + file_length, len(ordered_files))
                        )
                    ):
                        if start_idx + file_length <= len(ordered_files):
                            for i in range(file_length):
                                ordered_files[start_idx + i] = current_file[0]
                            original_positions = [
                                i
                                for i, x in enumerate(ordered_files)
                                if x == current_file[0]
                            ][-file_length:]
                            for pos in original_positions:
                                ordered_files[pos] = None
                            break

            current_file = []
            current_item = item

        if item is not None:
            current_file.append(item)

    checksum = 0
    for index, item in enumerate(ordered_files):
        if item is not None:
            checksum += index * item

    return checksum
