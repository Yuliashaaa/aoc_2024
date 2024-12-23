import re
from pathlib import Path


def parse_machine_configuration(configuration):
    """Parses a single claw machine's configuration from the input."""
    lines = configuration.strip().split('\n')
    button_a = list(map(int, re.findall(r'Button A: X\+(\d+), Y\+(\d+)', lines[0])[0]))
    button_b = list(map(int, re.findall(r'Button B: X\+(\d+), Y\+(\d+)', lines[1])[0]))
    prize_location = list(map(int, re.findall(r'Prize: X=(\d+), Y=(\d+)', lines[2])[0]))

    return button_a, button_b, prize_location


def is_prize_reachable(button_a, button_b, prize_location, max_presses=100):
    """Determines if a prize is reachable for a given machine configuration."""
    min_cost = float('inf')

    for presses_a in range(max_presses):
        for presses_b in range(max_presses):
            x_movement = button_a[0] * presses_a + button_b[0] * presses_b
            y_movement = button_a[1] * presses_a + button_b[1] * presses_b

            if (x_movement, y_movement) == tuple(prize_location):
                cost = presses_a * 3 + presses_b * 1
                min_cost = min(min_cost, cost)

    return min_cost if min_cost != float('inf') else None


def calculate_minimum_cost(input_file):
    """Calculates the minimum tokens required to win all possible prizes."""
    input_data = Path(input_file).read_text().strip().split('\n\n')
    total_cost = 0

    for configuration in input_data:
        button_a, button_b, prize_location = parse_machine_configuration(configuration)
        cost = is_prize_reachable(button_a, button_b, prize_location)
        if cost is not None:
            total_cost += cost

    return total_cost


if __name__ == '__main__':
    input_path = 'input.txt'
    total_tokens_spent = calculate_minimum_cost(input_path)
    print(f'Minimum tokens required to win all prizes: {total_tokens_spent}')
