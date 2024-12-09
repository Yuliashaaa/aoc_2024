from functools import lru_cache
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


@lru_cache(None)
def evaluate_expression(numbers, operators):
    """Evaluates an expression using numbers and operators in left-to-right order.

    Uses memoization to cache results of the same combination of numbers and operators.
    """
    result = numbers[0]

    for i, operator in enumerate(operators):
        if operator == '+':
            result += numbers[i + 1]
        elif operator == '*':
            result *= numbers[i + 1]
        elif operator == '||':
            result = int(f'{result}{numbers[i + 1]}')

    return result


def is_valid_equation(test_value, numbers):
    """Determines if the test value can be achieved by inserting operators.

    Uses backtracking with memoization and pruning.
    """

    def backtrack(index, current_value):  # NOQA: ANN202
        if index == len(numbers) - 1:
            return current_value == test_value

        next_num = numbers[index + 1]
        for operator in ('+', '*', '||'):
            if operator == '+':
                next_value = current_value + next_num
            elif operator == '*':
                next_value = current_value * next_num
            elif operator == '||':
                next_value = int(f'{current_value}{next_num}')

            if next_value > test_value:
                continue
            if backtrack(index + 1, next_value):
                return True

        return False

    # Start backtracking from the first number
    return backtrack(0, numbers[0])


def total_calibration_result(file_path):
    """Calculates the total calibration result from valid equations."""
    equations = parse_input(file_path)
    total = 0

    for test_value, numbers in equations:
        if is_valid_equation(test_value, tuple(numbers)):
            total += test_value

    return total


input_path = Path('input.txt')
if input_path.exists():
    result = total_calibration_result(input_path)
    print(f'Total calibration result: {result}')
else:
    print(f'File {input_path} does not exist.')
