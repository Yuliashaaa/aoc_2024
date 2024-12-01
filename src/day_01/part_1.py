from pathlib import Path


def read_input_file(file_path):
    """Reads the input file and returns two lists of integers representing the left and right columns."""
    left_list = []
    right_list = []

    try:
        path = Path(file_path)
        with path.open('r') as file:
            for line in file:
                left, right = map(int, line.split())
                left_list.append(left)
                right_list.append(right)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except ValueError:
        print('Error: Invalid file format.')

    return left_list, right_list


def calculate_total_distance(left_list, right_list):
    """Calculates the total distance between two lists of integers based on the smallest-to-smallest pairing rule."""
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    return sum(abs(l - r) for l, r in zip(left_sorted, right_sorted, strict=False))


if __name__ == '__main__':
    input_file = 'input.txt'
    left_list, right_list = read_input_file(input_file)

    if left_list and right_list:
        total_distance = calculate_total_distance(left_list, right_list)
        print(f'The total distance between the lists is: {total_distance}')
