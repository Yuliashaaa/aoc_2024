from pathlib import Path


def count_xmas_patterns(grid, patterns):
    """Counts the occurrences of X-MAS patterns in the grid.

    Each X-MAS pattern consists of two diagonal MAS (or SAM) sequences forming an 'X'.
    """
    rows, cols = len(grid), len(grid[0])
    total_count = 0

    def is_valid_xmas(x, y):  # NOQA: ANN202
        if not (0 < x < cols - 1 and 0 < y < rows - 1):
            return False  # Outside bounds where an X pattern can exist

        for pattern1 in patterns:
            for pattern2 in patterns:
                if (
                    f'{grid[y+1][x+1]}{grid[y][x]}{grid[y-1][x-1]}' == pattern1
                    and f'{grid[y-1][x+1]}{grid[y][x]}{grid[y+1][x-1]}' == pattern2
                ):
                    return True
        return False

    # Traverse the grid
    for r in range(rows):
        for c in range(cols):
            if is_valid_xmas(c, r):
                total_count += 1

    return total_count


if __name__ == '__main__':
    input_path = Path('input.txt')
    with input_path.open() as f:
        grid = [line.strip() for line in f]

    xmas_patterns = ('MAS', 'SAM')
    result = count_xmas_patterns(grid, xmas_patterns)
    print(f'The X-MAS pattern appears {result} times.')
