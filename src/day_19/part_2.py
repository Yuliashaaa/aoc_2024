from functools import lru_cache
from pathlib import Path


def parse_input(file_path):
    """Reads and parses the input file."""
    input_file = Path(file_path)
    if not input_file.exists():
        error_message = f"Input file '{file_path}' not found."
        raise FileNotFoundError(error_message)

    with input_file.open('r') as f:
        sections = f.read().strip().split('\n\n')

    patterns = sections[0].split(', ')
    designs = sections[1].split('\n')

    return patterns, designs


@lru_cache(None)
def count_ways(patterns, design):
    """Recursively counts the number of ways to construct the design using the patterns."""
    if not design:
        return 1

    total_ways = 0
    for pattern in patterns:
        if design.startswith(pattern):
            remaining_design = design[len(pattern) :]
            total_ways += count_ways(patterns, remaining_design)

    return total_ways


def total_arrangements(file_path):
    """Calculates the total number of ways to construct all designs."""
    patterns, designs = parse_input(file_path)
    patterns_tuple = tuple(patterns)
    total = 0

    for design in designs:
        total += count_ways(patterns_tuple, design)

    return total


def main():  # NOQA: D103
    input_file = 'input.txt'
    total = total_arrangements(input_file)
    print(total)


if __name__ == '__main__':
    main()
