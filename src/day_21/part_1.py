from itertools import permutations, product
from pathlib import Path

input_file = Path('input.txt')
with input_file.open() as file:
    lines = file.read().strip().split('\n')

# Numeric keypad layout with positions
NUMERIC_KEYPAD = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2),
}

# Directional keypad layout with positions
DIRECTION_KEYPAD = {'^': (0, 1), 'A': (0, 2), '<': (1, 0), 'v': (1, 1), '>': (1, 2)}

# Direction deltas for moving the robotic arm
DIRECTION_DELTA = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}


def generate_possible_sequences(code, keypad):
    """Generate all possible sequences to press the given code on the specified keypad."""
    sequences = []
    current_position = keypad['A']

    for char in code:
        target_position = keypad[char]
        row_diff = target_position[0] - current_position[0]
        col_diff = target_position[1] - current_position[1]
        moves = ''

        if row_diff > 0:
            moves += 'v' * row_diff
        elif row_diff < 0:
            moves += '^' * -row_diff
        if col_diff > 0:
            moves += '>' * col_diff
        elif col_diff < 0:
            moves += '<' * -col_diff

        raw_combos = {''.join(p) + 'A' for p in permutations(moves)}
        valid_combos = []

        for combo in raw_combos:
            row, col = current_position
            is_valid = True
            for move in combo[:-1]:  # Skip the last 'A'
                row_delta, col_delta = DIRECTION_DELTA[move]
                row, col = row + row_delta, col + col_delta
                if (row, col) not in keypad.values():
                    is_valid = False
                    break
            if is_valid:
                valid_combos.append(combo)

        sequences.append(valid_combos)
        current_position = target_position

    return [''.join(seq) for seq in product(*sequences)]


def find_shortest_sequence(code):
    """Find the shortest sequence of button presses for a given code."""
    valid_sequences1 = generate_possible_sequences(code, NUMERIC_KEYPAD)
    valid_sequences2 = []

    for seq in valid_sequences1:
        valid_sequences2.extend(generate_possible_sequences(seq, DIRECTION_KEYPAD))

    valid_sequences3 = []

    for seq in valid_sequences2:
        valid_sequences3.extend(generate_possible_sequences(seq, DIRECTION_KEYPAD))

    return min(len(seq) for seq in valid_sequences3)


def calculate_total_complexity():
    """Calculate the total complexity of typing all the codes."""
    total_complexity = 0

    for line in lines:
        code = line.strip()
        numeric_part = int(code[:-1])
        shortest_sequence_length = find_shortest_sequence(code)
        total_complexity += shortest_sequence_length * numeric_part
        print(f'Code: {code}, Shortest Sequence Length: {shortest_sequence_length}, Numeric Part: {numeric_part}')

    return total_complexity


total_complexity = calculate_total_complexity()
print(f'Total Complexity: {total_complexity}')
