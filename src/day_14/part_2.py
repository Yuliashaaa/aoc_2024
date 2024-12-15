import re
from pathlib import Path


def parse(line):
    """Parse a line of input to extract position and velocity."""
    pattern = r'p=(-?\d+,-?\d+) v=(-?\d+,-?\d+)'
    matches = re.match(pattern, line)

    if matches is None:
        print(f'Warning: Line did not match expected pattern: {line}')
        return None

    matches = matches.groups()
    p = matches[0].split(',')
    v = matches[1].split(',')

    return [(int(p[0]), int(p[1])), (int(v[0]), int(v[1]))]


def move(robot, steps, rows, cols):
    """Move a robot's position based on its velocity and steps. Wrap the position within the grid dimensions."""
    pos, vel = robot

    return (pos[0] + steps * vel[0]) % cols, (pos[1] + steps * vel[1]) % rows


def move_all(robots, steps, rows, cols):
    """Move all robots to their positions at a given step."""
    return [move(robot, steps, rows, cols) for robot in robots]


def find_largest_connected_region(robots_pos):
    """Find the size of the largest connected region of robots."""
    visited = set()
    largest_region_size = 0

    for pos in robots_pos:
        if pos in visited:
            continue

        region_size = 0
        stack = [pos]

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            region_size += 1

            x, y = current
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                neighbor = (x + dx, y + dy)
                if neighbor in robots_pos and neighbor not in visited:
                    stack.append(neighbor)

        largest_region_size = max(largest_region_size, region_size)

    return largest_region_size


def print_grid(robots_pos, rows, cols):
    """Print the grid with robots' positions marked as '#' ."""
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    for x, y in robots_pos:
        grid[y][x] = '#'

    for row in grid:
        print(''.join(row))


def main(input_file_path, rows, cols):
    """Main function to find and display the largest connected region."""
    input_data = Path(input_file_path).read_text()
    robots = [parse(line) for line in input_data.split('\n') if parse(line) is not None]
    max_size = 0
    best_time = 0

    for steps in range(1, 100000):
        robots_pos = move_all(robots, steps, rows, cols)
        size = find_largest_connected_region(robots_pos)

        if size > max_size:
            max_size = size
            best_time = steps

            print(f'Time: {best_time}, Largest Region Size: {max_size}')
            print_grid(robots_pos, rows, cols)

    print(f'Optimal time: {best_time}, Largest region: {max_size}')


if __name__ == '__main__':
    input_file_path = 'input.txt'
    rows = 103
    cols = 101

    main(input_file_path, rows, cols)
