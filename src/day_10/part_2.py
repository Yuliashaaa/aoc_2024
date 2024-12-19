from pathlib import Path


def parse_input(file_path: Path) -> list[list[int]]:
    """Parses the input topographic map from a file into a 2D list of integers."""
    with file_path.open() as f:
        return [list(map(int, line.strip())) for line in f]


def find_trailheads(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Finds all trailhead positions (positions with height 0) in the grid."""
    trailheads = []

    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 0:
                trailheads.append((r, c))

    return trailheads


def count_distinct_trails(grid: list[list[int]], start: tuple[int, int]) -> int:
    """Counts the number of distinct hiking trails starting from a given trailhead. Uses DFS."""
    rows, cols = len(grid), len(grid[0])
    memo: dict[tuple[int, int], int] = {}

    def dfs(r: int, c: int) -> int:
        """Recursively explores all valid paths from the current position. Memoization is used here too."""
        if (r, c) in memo:
            return memo[(r, c)]

        if grid[r][c] == 9:  # NOQA: PLR2004
            return 1

        total_trails = 0

        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == grid[r][c] + 1:
                total_trails += dfs(nr, nc)

        memo[(r, c)] = total_trails
        return total_trails

    return dfs(*start)


def calculate_total_rating(grid: list[list[int]]) -> int:
    """Calculates the sum of ratings for all trailheads in the grid."""
    trailheads = find_trailheads(grid)
    total_rating = 0

    for trailhead in trailheads:
        total_rating += count_distinct_trails(grid, trailhead)

    return total_rating


def main(file_path: str) -> int:  # NOQA: D103
    grid = parse_input(Path(file_path))
    return calculate_total_rating(grid)


if __name__ == '__main__':
    input_file = 'input.txt'
    result = main(input_file)
    print(f'Total Rating: {result}')
