from pathlib import Path


def load_grid(file_path):
    """Loads the grid of garden plots from the input file."""
    return Path(file_path).read_text().strip().split('\n')


def is_within_grid(x, y, grid_size):
    """Checks if the given coordinates are within the grid bounds."""
    return 0 <= x < grid_size and 0 <= y < grid_size


def find_contiguous_plots(grid):
    """Finds all contiguous plots in the grid."""
    grid_size = len(grid)
    visited = set()
    plots = []
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left

    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in visited:
                continue

            stack = [(i, j)]
            current_plot_cells = []
            plot_type = grid[i][j]

            while stack:
                x, y = stack.pop()
                if (x, y) in visited or not is_within_grid(x, y, grid_size) or grid[x][y] != plot_type:
                    continue

                visited.add((x, y))
                current_plot_cells.append((x, y))

                for dx, dy in directions:
                    stack.append((x + dx, y + dy))

            plots.append((plot_type, current_plot_cells))

    return plots


def calculate_plot_perimeter(plot, grid_size):
    """Calculates the perimeter of a given plot."""
    plot_set = set(plot)

    def check_neighbors(coords):  # NOQA: ANN202
        return [int((x, y) in plot_set) for x, y in coords]

    min_row, max_row = grid_size, -1
    min_col, max_col = grid_size, -1

    for x, y in plot_set:
        min_row, max_row = min(min_row, x), max(max_row, x)
        min_col, max_col = min(min_col, y), max(max_col, y)

    perimeter = 0

    for i in range(min_row - 1, max_row + 2):
        for j in range(min_col - 1, max_col + 2):
            neighbors = check_neighbors([(i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1)])
            has_single_corner = neighbors in (
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                [1, 1, 1, 0],
                [1, 1, 0, 1],
                [1, 0, 1, 1],
                [0, 1, 1, 1],
            )
            has_double_corner = neighbors in ([1, 0, 0, 1], [0, 1, 1, 0])

            perimeter += has_single_corner + has_double_corner * 2

    return perimeter


def calculate_total_fencing_cost(grid):
    """Calculates the total cost of fencing all plots."""
    grid_size = len(grid)
    plots = find_contiguous_plots(grid)
    total_cost = 0

    for plot_type, plot_cells in plots:  # NOQA: B007
        plot_perimeter = calculate_plot_perimeter(plot_cells, grid_size)
        total_cost += plot_perimeter * len(plot_cells)

    return total_cost


if __name__ == '__main__':
    input_file = 'input.txt'
    grid = load_grid(input_file)
    total_cost = calculate_total_fencing_cost(grid)
    print(f'Total price of fencing all regions: {total_cost}')
