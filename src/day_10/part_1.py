from collections import deque
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


def bfs_trail_score(grid: list[list[int]], start: tuple[int, int]) -> int:
    """Find all reachable positions with height 9. Returns the count of reachable height-9 positions."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([start])
    visited.add(start)
    reachable_nines = 0

    while queue:
        r, c = queue.popleft()

        if grid[r][c] == 9:  # NOQA: PLR2004
            reachable_nines += 1

        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == grid[r][c] + 1:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return reachable_nines


def calculate_total_score(grid: list[list[int]]) -> int:
    """Calculates the total score of all trailheads on the grid."""
    trailheads = find_trailheads(grid)
    total_score = 0

    for trailhead in trailheads:
        total_score += bfs_trail_score(grid, trailhead)

    return total_score


def main(file_path: str) -> int:  # NOQA: D103
    grid = parse_input(Path(file_path))

    return calculate_total_score(grid)


if __name__ == '__main__':
    input_file = 'input.txt'
    result = main(input_file)
    print(f'Total Score: {result}')
