from src.day_06.part_1 import find_position, move_guard, parse_map, turn_right


def simulate_with_obstruction(grid, obstruction_y, obstruction_x):
    """Simulates guard movement with an obstruction at the specified position.

    Returns True if the guard gets stuck in a loop.
    """
    obstacle = '#'
    direction = 'up'
    y, x = find_position(grid, '^')
    visited_states = set()

    grid[obstruction_y][obstruction_x] = obstacle  # Place the obstruction

    while True:
        # Track current state (position + direction)
        state = (y, x, direction)
        if state in visited_states:
            # Restore the grid before returning
            grid[obstruction_y][obstruction_x] = '.'
            return True
        visited_states.add(state)

        # Move the guard
        new_y, new_x = move_guard(y, x, direction)
        if not (0 <= new_y < len(grid) and 0 <= new_x < len(grid[0])):
            break  # Guard leaves the grid

        if grid[new_y][new_x] == obstacle:
            direction = turn_right(direction)
        else:
            y, x = new_y, new_x

    # Restore the grid before returning
    grid[obstruction_y][obstruction_x] = '.'
    return False


def count_loop_positions(grid):
    """Counts all valid positions for placing an obstruction that causes the guard to get stuck in a loop."""
    start_y, start_x = find_position(grid, '^')
    valid_positions = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # Check if this is a valid position for the obstruction
            if grid[y][x] == '.' and (y, x) != (start_y, start_x) and simulate_with_obstruction(grid, y, x):
                valid_positions += 1

    return valid_positions


if __name__ == '__main__':
    input_file = 'input.txt'
    guard_map = parse_map(input_file)
    result = count_loop_positions(guard_map)
    print(f'There are {result} positions where the obstruction causes a loop.')
