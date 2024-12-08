from pathlib import Path


def parse_map(file_path):
    """Parses the input file to generate the guard map."""
    map_data = Path(file_path).read_text().strip()

    return [list(row) for row in map_data.split('\n')]


def find_position(grid, symbol):
    """Finds the position of a specific symbol (e.g., '^') in the grid."""
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == symbol:
                return row_index, col_index

    return None


def move_guard(y, x, direction):
    """Moves the guard in the current direction."""
    match direction:
        case 'up':
            return y - 1, x
        case 'down':
            return y + 1, x
        case 'left':
            return y, x - 1
        case 'right':
            return y, x + 1


def turn_right(direction):
    """Turns the guard 90 degrees to the right."""
    return {'up': 'right', 'right': 'down', 'down': 'left', 'left': 'up'}[direction]


def simulate_guard(grid):
    """Simulates the guard's movement and returns the count of distinct visited positions."""
    obstacle = '#'
    visited = 'X'

    # Initialize guard's starting position and direction
    start_symbol = '^'
    direction = 'up'
    start_position = find_position(grid, start_symbol)
    if not start_position:
        error_msg = "Guard starting position '{start_symbol}' not found."
        raise ValueError(error_msg.format(start_symbol=start_symbol))

    y, x = start_position
    grid[y][x] = visited
    visited_positions = {(y, x)}

    while True:
        new_y, new_x = move_guard(y, x, direction)

        if not (0 <= new_y < len(grid) and 0 <= new_x < len(grid[0])):
            # Guard leaves the grid
            break

        if grid[new_y][new_x] == obstacle:
            # Turn right when encountering an obstacle
            direction = turn_right(direction)
        else:
            # Mark the current position as visited and move forward
            grid[y][x] = visited
            y, x = new_y, new_x
            visited_positions.add((y, x))

    return len(visited_positions)


if __name__ == '__main__':
    input_file = 'input.txt'
    guard_map = parse_map(input_file)
    result = simulate_guard(guard_map)
    print(f'The guard visits {result} distinct positions.')
