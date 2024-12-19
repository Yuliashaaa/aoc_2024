from collections import deque
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


def is_design_possible(patterns, design):
    """Determines if the given design can be constructed from the available patterns."""
    queue = deque([design])
    visited = set()
    visited.add(design)

    while queue:
        current = queue.popleft()

        if not current:
            return True

        for pattern in patterns:
            if current.startswith(pattern):
                new_state = current[len(pattern) :]
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)

    return False


def count_possible_designs(file_path):
    """Counts how many designs can be constructed from the available patterns."""
    patterns, designs = parse_input(file_path)
    count = 0

    for design in designs:
        if is_design_possible(patterns, design):
            count += 1

    return count


def main():  # NOQA: D103
    input_file = 'input.txt'
    possible_count = count_possible_designs(input_file)
    print(possible_count)


if __name__ == '__main__':
    main()
