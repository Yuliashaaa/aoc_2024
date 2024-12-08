from collections import defaultdict
from math import gcd
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


def add_collinear_points(positions, antinodes, grid_width, grid_height):
    """Adds all collinear points for pairs of positions to the antinodes set."""
    n = len(positions)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = positions[i]
            x2, y2 = positions[j]

            # Compute step size using GCD to reduce the vector
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)
            dx, dy = dx // g, dy // g

            # Generate all points along the line in both directions
            for step in range(-grid_width * grid_height, grid_width * grid_height + 1):
                x, y = x1 + step * dx, y1 + step * dy
                if 0 <= x < grid_width and 0 <= y < grid_height:
                    antinodes.add((x, y))


def calculate_antinodes(frequency_positions, grid_width, grid_height):
    """Calculates unique antinodes based on antenna positions (Part 2 logic)."""
    antinodes = set()

    for positions in frequency_positions.values():
        n = len(positions)
        if n < 2:  # NOQA: PLR2004
            continue

        antinodes.update(positions)
        add_collinear_points(positions, antinodes, grid_width, grid_height)

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
