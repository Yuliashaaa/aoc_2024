from collections import defaultdict
from pathlib import Path


def parse_input(file_path):
    """Parses the input file and returns a dictionary mapping frequencies to their positions."""
    frequency_positions = defaultdict(list)
    with file_path.open('r') as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char.isalnum():
                    frequency_positions[char].append((x, y))

    return frequency_positions, x + 1, y + 1


def calculate_antinodes(frequency_positions, grid_width, grid_height):
    """Calculates unique antinodes based on antenna positions."""
    antinodes = set()

    for positions in frequency_positions.values():
        n = len(positions)
        if n < 2:  # NOQA: PLR2004
            continue

        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                dx, dy = x2 - x1, y2 - y1

                # Antinode 1: Extend beyond (x2, y2)
                x3, y3 = x2 + dx, y2 + dy
                if 0 <= x3 < grid_width and 0 <= y3 < grid_height:
                    antinodes.add((x3, y3))

                # Antinode 2: Extend beyond (x1, y1)
                x4, y4 = x1 - dx, y1 - dy
                if 0 <= x4 < grid_width and 0 <= y4 < grid_height:
                    antinodes.add((x4, y4))

                # Midpoint check for valid "twice the distance" rule
                if dx % 2 == dy % 2 == 0:
                    mid_x, mid_y = x1 + dx // 2, y1 + dy // 2
                    if 0 <= mid_x < grid_width and 0 <= mid_y < grid_height:
                        antinodes.add((mid_x, mid_y))

    return antinodes


def count_unique_antinodes(file_path):
    """Main function to parse input, calculate antinodes, and return the count of unique antinode locations."""
    frequency_positions, grid_width, grid_height = parse_input(file_path)
    antinodes = calculate_antinodes(frequency_positions, grid_width, grid_height)

    return len(antinodes)


input_path = Path('input.txt')
if input_path.exists():
    result = count_unique_antinodes(input_path)
    print(f'Number of unique antinode locations: {result}')
else:
    print(f'File {input_path} does not exist.')
