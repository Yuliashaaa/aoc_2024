from pathlib import Path

# Define constants for direction mappings
DIRECTIONS = {'<': (0, -1), 'v': (1, 0), '>': (0, 1), '^': (-1, 0)}


def is_within_grid(x, y, rows, cols):  # NOQA: D103
    return 0 <= x < rows and 0 <= y < cols


def process_movement_step(grid, robot_pos, direction):  # NOQA: D103
    rows, cols = len(grid), len(grid[0])
    dx, dy = direction
    robot_x, robot_y = robot_pos
    new_robot_x, new_robot_y = robot_x + dx, robot_y + dy

    if not is_within_grid(new_robot_x, new_robot_y, rows, cols):
        return robot_pos

    if grid[new_robot_x][new_robot_y] == 'O':
        box_x, box_y = new_robot_x, new_robot_y

        while is_within_grid(box_x, box_y, rows, cols):
            box_x += dx
            box_y += dy

            if not is_within_grid(box_x, box_y, rows, cols) or grid[box_x][box_y] == '#':
                break

            if grid[box_x][box_y] == '.':
                grid[box_x][box_y] = 'O'
                grid[new_robot_x][new_robot_y] = '@'
                grid[robot_x][robot_y] = '.'

                return (new_robot_x, new_robot_y)

    elif grid[new_robot_x][new_robot_y] == '.':
        grid[new_robot_x][new_robot_y] = '@'
        grid[robot_x][robot_y] = '.'

        return (new_robot_x, new_robot_y)

    return robot_pos


def calculate_gps_sum(grid):  # NOQA: D103
    gps_sum = 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'O':
                gps_sum += 100 * i + j

    return gps_sum


def main():  # NOQA: D103
    input_path = Path('input.txt')
    input_data = input_path.read_text().strip()
    grid_data, movement_sequence = input_data.split('\n\n')
    grid = [list(line) for line in grid_data.splitlines()]
    movement_sequence = movement_sequence.replace('\n', '')
    robot_position = None

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                robot_position = (i, j)
                break
        if robot_position:
            break

    for move in movement_sequence:
        robot_position = process_movement_step(grid, robot_position, DIRECTIONS[move])

    gps_sum = calculate_gps_sum(grid)
    print('\n'.join(''.join(row) for row in grid))
    print(gps_sum)


if __name__ == '__main__':
    main()
