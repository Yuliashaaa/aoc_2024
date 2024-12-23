import re
from pathlib import Path


def parse_machine_configuration(configuration):
    """Parses a single claw machine's configuration from the input."""
    lines = configuration.strip().split('\n')
    button_a = list(map(int, re.findall(r'Button A: X\+(\d+), Y\+(\d+)', lines[0])[0]))
    button_b = list(map(int, re.findall(r'Button B: X\+(\d+), Y\+(\d+)', lines[1])[0]))
    prize_location = list(map(int, re.findall(r'Prize: X=(\d+), Y=(\d+)', lines[2])[0]))

    return button_a, button_b, prize_location


def adjust_prize_location(prize_location):
    """Adjusts the prize location by adding 10^13 to both X and Y coordinates."""
    offset = 10**13

    return [prize_location[0] + offset, prize_location[1] + offset]


def verify_solution(button_a, button_b, prize_location, presses_a, presses_b):
    """Verifies if the given combination of button presses reaches the prize location."""
    x_movement = button_a[0] * presses_a + button_b[0] * presses_b
    y_movement = button_a[1] * presses_a + button_b[1] * presses_b

    return (x_movement, y_movement) == tuple(prize_location)


def calculate_minimum_cost(input_file):
    """Calculates the minimum tokens required to win all possible prizes with adjusted prize locations."""
    input_data = Path(input_file).read_text().strip().split('\n\n')
    total_cost = 0

    for configuration in input_data:
        button_a, button_b, prize_location = parse_machine_configuration(configuration)
        prize_location = adjust_prize_location(prize_location)
        denominator = button_b[1] * button_a[0] - button_b[0] * button_a[1]

        if denominator == 0:
            # The movements are linearly dependent
            continue

        presses_a = (prize_location[0] * button_b[1] - button_b[0] * prize_location[1]) // denominator
        presses_b = (prize_location[1] - button_a[1] * presses_a) // button_b[1]

        if (
            presses_a >= 0
            and presses_b >= 0
            and verify_solution(button_a, button_b, prize_location, presses_a, presses_b)
        ):
            total_cost += 3 * presses_a + presses_b

    return total_cost


if __name__ == '__main__':
    input_path = 'input.txt'
    total_tokens_spent = calculate_minimum_cost(input_path)
    print(f'Minimum tokens required to win all prizes: {total_tokens_spent}')
