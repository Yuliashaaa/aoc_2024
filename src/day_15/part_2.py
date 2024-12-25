from pathlib import Path

input_path = Path('input.txt')
with input_path.open() as fin:
    parts = fin.read().strip().split('\n\n')
    initial_grid = [list(line) for line in parts[0].split('\n')]
    robot_moves = parts[1].replace('\n', '')

original_height = len(initial_grid)
original_width = len(initial_grid[0])

directions = {'<': (0, -1), 'v': (1, 0), '>': (0, 1), '^': (-1, 0)}

expanded_grid = []
for row in initial_grid:
    expanded_row = []
    for tile in row:
        if tile == '#':
            expanded_row.extend(['#', '#'])
        elif tile == 'O':
            expanded_row.extend(['[', ']'])
        elif tile == '.':
            expanded_row.extend(['.', '.'])
        elif tile == '@':
            expanded_row.extend(['@', '.'])
    expanded_grid.append(expanded_row)

robot_position = None
box_positions = []
wall_positions = set()

for i, row in enumerate(expanded_grid):
    for j, tile in enumerate(row):
        if tile == '@':
            robot_position = (i, j)
        elif tile == '[':
            box_positions.append((i, j))
        elif tile == '#':
            wall_positions.add((i, j))


def is_within_bounds(i, j):  # NOQA: D103
    return 0 <= i < len(expanded_grid) and 0 <= j < len(expanded_grid[0])


def move_robot(direction):  # NOQA: D103
    global robot_position, box_positions  # NOQA: PLW0603, PLW0602
    di, dj = direction
    new_robot_i, new_robot_j = robot_position[0] + di, robot_position[1] + dj

    if not is_within_bounds(new_robot_i, new_robot_j) or (new_robot_i, new_robot_j) in wall_positions:
        return

    pushing_boxes = []
    for box in box_positions:
        if box == (new_robot_i, new_robot_j) or box == (new_robot_i, new_robot_j - 1):
            pushing_boxes.append(box)  # NOQA: PERF401

    can_move_boxes = True
    seen = set()
    stack = pushing_boxes[:]

    while stack:
        current_box = stack.pop()
        seen.add(current_box)
        next_box_i, next_box_j = current_box[0] + di, current_box[1] + dj

        if (
            not is_within_bounds(next_box_i, next_box_j)
            or (next_box_i, next_box_j) in wall_positions
            or (next_box_i, next_box_j + 1) in wall_positions
        ):
            can_move_boxes = False
            break

        for neighbor in ((next_box_i, next_box_j), (next_box_i, next_box_j - 1), (next_box_i, next_box_j + 1)):
            if neighbor in box_positions and neighbor not in seen:
                stack.append(neighbor)

    if can_move_boxes:
        for i, box in enumerate(box_positions):
            if box in seen:
                box_positions[i] = (box[0] + di, box[1] + dj)
        robot_position = (new_robot_i, new_robot_j)


for move in robot_moves:
    move_robot(directions[move])


def calculate_gps_coordinate(i, j):  # NOQA: D103
    return i * 100 + j


final_gps_sum = sum(calculate_gps_coordinate(i, j) for i, j in box_positions)

print(final_gps_sum)
