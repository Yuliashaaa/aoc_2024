from pathlib import Path


def count_word_occurrences(grid, word):
    """Counts the occurrences of a given word in a grid, considering all possible directions."""
    rows, cols = len(grid), len(grid[0])
    word_length = len(word)
    directions = [
        (0, 1),  # Horizontal (right)
        (1, 0),  # Vertical (down)
        (1, 1),  # Diagonal (down-right)
        (1, -1),  # Diagonal (down-left)
    ]
    total_count = 0

    # Helper function to check if the word exists in a specific direction
    def check_direction(x, y, dx, dy):  # NOQA: ANN202
        for i in range(word_length):
            nx, ny = x + i * dx, y + i * dy
            if nx < 0 or ny < 0 or nx >= rows or ny >= cols or grid[nx][ny] != word[i]:
                return False
        return True

    for r in range(rows):
        for c in range(cols):
            for dx, dy in directions:
                if check_direction(r, c, dx, dy):
                    total_count += 1
                if check_direction(r, c, -dx, -dy):  # Check reversed direction
                    total_count += 1

    return total_count


if __name__ == '__main__':
    input_path = Path('input.txt')
    with input_path.open() as f:
        grid = [line.strip() for line in f]

    target_word = 'XMAS'
    result = count_word_occurrences(grid, target_word)
    print(f"The word '{target_word}' appears {result} times.")
