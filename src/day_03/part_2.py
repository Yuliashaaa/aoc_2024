import re
from pathlib import Path


def parse_and_calculate_with_conditions(file_path):
    """Reads the input file, processes instructions, calculates results for enabled instructions, returns the sum."""
    path = Path(file_path)
    with path.open() as f:
        data = f.read()

    mul_pattern = r'mul\(\s*(\d+)\s*,\s*(\d+)\s*\)'
    condition_pattern = r"do\(\)|don't\(\)"
    tokens = re.split(f'({condition_pattern})', data)

    mul_enabled = True
    total_sum = 0

    for token in tokens:
        token = token.strip()  # NOQA: PLW2901

        if token == 'do()':  # NOQA: S105
            mul_enabled = True
        elif token == "don't()":  # NOQA: S105
            mul_enabled = False
        elif mul_enabled:
            matches = re.findall(mul_pattern, token)
            total_sum += sum(int(x) * int(y) for x, y in matches)

    return total_sum


if __name__ == '__main__':
    input_file = 'input.txt'
    result = parse_and_calculate_with_conditions(input_file)
    print(f"Total sum of enabled 'mul' results: {result}")
