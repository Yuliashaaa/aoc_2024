from collections import deque
from pathlib import Path


def parse_input(file_path):
    """Read and parse the input file."""
    input_file = Path(file_path)
    with input_file.open('r') as f:
        lines = f.read().strip().split('\n')

    # Parse coordinates
    return [tuple(map(int, line.split(','))) for line in lines]


def find_shortest_path(grid):
    """Check if a path exists from (0, 0) to (70, 70)."""
    grid_size = len(grid)
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)

    if '#' in (grid[0][0], grid[grid_size - 1][grid_size - 1]):
        return False  # Path is blocked at start or goal

    # Directions for moving in the grid
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])
    visited = set()
    visited.add(start)

    while queue:
        x, y = queue.popleft()

        if (x, y) == goal:
            return True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[ny][nx] == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return False


def find_first_blocking_byte(grid_size, byte_positions):
    """Find the first byte that blocks the path to the exit."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    for x, y in byte_positions:
        grid[y][x] = '#'

        # Check if the path is still accessible
        if not find_shortest_path(grid):
            return f'{x},{y}'  # Return the coordinates of the blocking byte

    return None


def main():  # NOQA: D103
    file_path = 'input.txt'
    grid_size = 71  # Grid is 0 to 70, so size is 71x71

    byte_positions = parse_input(file_path)
    result = find_first_blocking_byte(grid_size, byte_positions)
    print(result)


if __name__ == '__main__':
    main()
