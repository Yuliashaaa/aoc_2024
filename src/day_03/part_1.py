import re
from pathlib import Path


def parse_and_calculate(file_path):
    """Reads the input file, extracts valid 'mul(X, Y)' instructions, calculates their results, and returns the sum."""
    path = Path(file_path)
    with path.open() as f:
        data = f.read()

    pattern = r'mul\(\s*(\d+)\s*,\s*(\d+)\s*\)'
    matches = re.findall(pattern, data)

    return sum(int(x) * int(y) for x, y in matches)


if __name__ == '__main__':
    input_file = 'input.txt'
    result = parse_and_calculate(input_file)
    print(f'Total sum of results: {result}')
