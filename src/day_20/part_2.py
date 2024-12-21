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
            si, sj = i, j
        elif grid[i][j] == 'E':
            ei, ej = i, j


def bfs(start_i, start_j):  # NOQA: D103
    queue = deque([(start_i, start_j)])
    visited = {(start_i, start_j)}
    parent = {(start_i, start_j): None}

    while queue:
        i, j = queue.popleft()

        if (i, j) == (ei, ej):
            break

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if in_grid(ni, nj) and (ni, nj) not in visited and grid[ni][nj] != '#':
                visited.add((ni, nj))
                parent[(ni, nj)] = (i, j)
                queue.append((ni, nj))

    path = []
    current = (ei, ej)

    while current != (si, sj):
        path.append(current)
        current = parent[current]
    path.append((si, sj))
    path.reverse()

    return path


path = bfs(si, sj)
og_path_length = len(path) - 1
times = {coord: og_path_length - idx for idx, coord in enumerate(path)}
max_len = 20
counts = defaultdict(int)
saved_cheats = {}

for t, (i, j) in enumerate(tqdm(path, ncols=80)):
    for di in range(i - max_len, i + max_len + 1):
        for dj in range(j - max_len, j + max_len + 1):
            time_used = abs(di - i) + abs(dj - j)

            if not in_grid(di, dj) or time_used > max_len or grid[di][dj] == '#':
                continue

            rem_t = times.get((di, dj), None)

            if rem_t is None:
                continue

            saved_time = og_path_length - (t + rem_t + time_used)

            if saved_time >= 0:
                saved_cheats[(i, j, di, dj)] = saved_time
                counts[saved_time] += 1

result = sum(1 for time in saved_cheats.values() if time >= 100)  # NOQA: PLR2004
print(result)
