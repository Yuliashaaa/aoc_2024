from functools import lru_cache
from itertools import combinations
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

# Directional movement deltas
DIRECTION_DELTA = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}


def generate_combinations(char_a, len_a, char_b, len_b):
    """Generate all combinations of moves with specified lengths."""
    for indices in combinations(range(len_a + len_b), r=len_a):
        result = [char_b] * (len_a + len_b)

        for idx in indices:
            result[idx] = char_a

        yield ''.join(result)


@lru_cache(None)
def generate_valid_sequences(start_char, end_char, is_directional):
    """Generate valid sequences of moves from one keypad character to another."""
    keypad = DIRECTION_KEYPAD if is_directional else NUMERIC_KEYPAD
    start_position = keypad[start_char]
    end_position = keypad[end_char]
    row_diff = end_position[0] - start_position[0]
    col_diff = end_position[1] - start_position[1]
    moves = []

    if row_diff > 0:
        moves += ['v', row_diff]
    else:
        moves += ['^', -row_diff]
    if col_diff > 0:
        moves += ['>', col_diff]
    else:
        moves += ['<', -col_diff]

    raw_combinations = {''.join(comb) + 'A' for comb in generate_combinations(*moves)}
    valid_combinations = []

    for comb in raw_combinations:
        current_row, current_col = start_position
        is_valid = True
        for move in comb[:-1]:  # Skip the last 'A'
            row_delta, col_delta = DIRECTION_DELTA[move]
            current_row, current_col = current_row + row_delta, current_col + col_delta
            if (current_row, current_col) not in keypad.values():
                is_valid = False
                break
        if is_valid:
            valid_combinations.append(comb)

    return valid_combinations


@lru_cache(None)
def get_move_cost(start_char, end_char, is_directional, depth=0):
    """Calculate the cost of moving from one character to another on the given keypad."""
    if depth == 0:
        if is_directional is None:
            error_message = 'Directionality is required'
            raise ValueError(error_message)
        return min(len(seq) for seq in generate_valid_sequences(start_char, end_char, True))  # NOQA: FBT003

    valid_sequences = generate_valid_sequences(start_char, end_char, is_directional)
    best_cost = float('inf')

    for seq in valid_sequences:
        seq = 'A' + seq  # NOQA: PLW2901
        cost = 0
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]
            cost += get_move_cost(a, b, True, depth - 1)  # NOQA: FBT003

        best_cost = min(best_cost, cost)

    return best_cost


def get_code_total_cost(code, depth):
    """Calculate the total cost of typing the given code."""
    code = 'A' + code
    total_cost = 0

    for i in range(len(code) - 1):
        a, b = code[i], code[i + 1]
        total_cost += get_move_cost(a, b, False, depth)  # NOQA: FBT003

    return total_cost


total_complexity = 0

for line in lines:
    total_complexity += get_code_total_cost(line, 25) * int(line[:-1])

print(total_complexity)
