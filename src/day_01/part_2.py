from collections import Counter

from src.day_01.part_1 import read_input_file


def calculate_similarity_score(left_list, right_list):
    """Calculates the similarity score based on how often each number in the left list appears in the right list."""
    right_counts = Counter(right_list)

    return sum(num * right_counts[num] for num in left_list)


if __name__ == '__main__':
    input_file = 'input.txt'
    left_list, right_list = read_input_file(input_file)

    if left_list and right_list:
        similarity_score = calculate_similarity_score(left_list, right_list)
        print(f'The similarity score between the lists is: {similarity_score}')
