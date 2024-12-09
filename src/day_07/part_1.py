from itertools import product
from pathlib import Path


def parse_input(file_path):
    """Reads the input file and returns a list of (test_value, numbers) tuples."""
    equations = []

    with file_path.open('r') as file:
        for line in file:
            test_value, numbers = line.strip().split(': ')
            test_value = int(test_value)
            numbers = list(map(int, numbers.split()))
            equations.append((test_value, numbers))

    return equations


def evaluate_expression(numbers, operators):
    """Evaluates the expression left-to-right given numbers and operators."""
    result = numbers[0]

    for i, operator in enumerate(operators):
        if operator == '+':
            result += numbers[i + 1]
        elif operator == '*':
            result *= numbers[i + 1]

    return result


def is_valid_equation(test_value, numbers):
    """Determines if the test value can be achieved by inserting operators between the numbers in the given order."""
    num_operators = len(numbers) - 1

    for operators in product('+-*', repeat=num_operators):
        if evaluate_expression(numbers, operators) == test_value:
            return True

    return False


def total_calibration_result(file_path):
    """Calculates the total calibration result from valid equations."""
    equations = parse_input(file_path)
    total = 0

    for test_value, numbers in equations:
        if is_valid_equation(test_value, numbers):
            total += test_value

    return total


input_path = Path('input.txt')
if input_path.exists():
    result = total_calibration_result(input_path)
    print(f'Total calibration result: {result}')
else:
    print(f'File {input_path} does not exist.')
