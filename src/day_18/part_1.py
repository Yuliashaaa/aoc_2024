from collections import deque
from pathlib import Path


def parse_input(file_path):
    """Read and parse the input file."""
    input_file = Path(file_path)

    with input_file.open('r') as f:
        lines = f.read().strip().split('\n')

    return [tuple(map(int, line.split(','))) for line in lines]


def simulate_falling_bytes(grid_size, byte_positions, num_bytes):
    """Simulate the first `num_bytes` bytes falling into the grid."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    for i, (x, y) in enumerate(byte_positions):
        if i >= num_bytes:
            break
        grid[y][x] = '#'

    return grid


def find_shortest_path(grid):
    """Find the shortest path."""
    grid_size = len(grid)
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)

    if '#' in (grid[0][0], grid[grid_size - 1][grid_size - 1]):
        return -1  # No path possible if start or goal is blocked

    # Directions for moving in the grid
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start, 0)])  # (current position, steps taken)
    visited = set()
    visited.add(start)

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == goal:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[ny][nx] == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))

    return -1


def main():  # NOQA: D103
    file_path = 'input.txt'
    grid_size = 71  # Grid is 0 to 70, so size is 71x71
    num_bytes = 1024  # Simulate first 1024 bytes

    byte_positions = parse_input(file_path)
    grid = simulate_falling_bytes(grid_size, byte_positions, num_bytes)
    shortest_path_length = find_shortest_path(grid)

    if shortest_path_length == -1:
        print('No path to the exit is possible.')
    else:
        print(f'The minimum number of steps to reach the exit is: {shortest_path_length}')


if __name__ == '__main__':
    main()
