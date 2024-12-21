from collections import defaultdict, deque
from pathlib import Path

from tqdm import tqdm

input_file = Path('input.txt')
grid = [list(line.strip()) for line in input_file.read_text().splitlines()]
N = len(grid)
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def in_grid(i, j):
    """Check if the coordinates (i, j) are within the grid bounds."""
    return 0 <= i < N and 0 <= j < N


for i in range(N):
    for j in range(N):
        if grid[i][j] == 'S':
            start_i, start_j = i, j
        elif grid[i][j] == 'E':
            end_i, end_j = i, j


def bfs(start_i, start_j):  # NOQA: D103
    queue = deque([(start_i, start_j)])
    visited = {(start_i, start_j)}
    parent = {(start_i, start_j): None}

    while queue:
        i, j = queue.popleft()

        if (i, j) == (end_i, end_j):
            break

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if in_grid(ni, nj) and (ni, nj) not in visited and grid[ni][nj] != '#':
                visited.add((ni, nj))
                parent[(ni, nj)] = (i, j)
                queue.append((ni, nj))

    path = []
    current = (end_i, end_j)

    while current != (start_i, start_j):
        path.append(current)
        current = parent[current]

    path.append((start_i, start_j))
    path.reverse()

    return path


path = bfs(start_i, start_j)
og_path_length = len(path) - 1
times = {coord: og_path_length - idx for idx, coord in enumerate(path)}
counts = defaultdict(int)
saved_cheats = {}

for t, (i, j) in enumerate(tqdm(path, ncols=80)):
    for di1, dj1 in directions:
        for di2, dj2 in directions:
            ni, nj = i + di1 + di2, j + dj1 + dj2
            if in_grid(ni, nj) and grid[ni][nj] != '#':
                rem_t = times[(ni, nj)]
                saved_cheats[(i, j, ni, nj)] = og_path_length - (t + rem_t + 2)

result = 0

for saved_time in saved_cheats.values():
    if saved_time >= 0:
        counts[saved_time] += 1
    if saved_time >= 100:  # NOQA: PLR2004
        result += 1

print(result)
