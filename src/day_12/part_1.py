from pathlib import Path


def load_grid(file_path):
    """Loads the grid of garden plots from the input file."""
    return Path(file_path).read_text().strip().split('\n')


def is_within_grid(x, y, grid_size):
    """Checks if the given coordinates are within the grid bounds."""
    return 0 <= x < grid_size and 0 <= y < grid_size


def explore_region(grid, start_x, start_y, visited):
    """Finds all plots in the same region as the starting plot."""
    stack = [(start_x, start_y)]
    region_cells = []
    plot_type = grid[start_x][start_y]

    while stack:
        x, y = stack.pop()

        if (x, y) in visited or not is_within_grid(x, y, len(grid)) or grid[x][y] != plot_type:
            continue

        visited.add((x, y))
        region_cells.append((x, y))

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            stack.append((x + dx, y + dy))

    return region_cells


def calculate_perimeter(grid, region_cells):
    """Calculates the perimeter of a region."""
    perimeter = 0

    for x, y in region_cells:
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbor_x, neighbor_y = x + dx, y + dy
            if not is_within_grid(neighbor_x, neighbor_y, len(grid)) or grid[neighbor_x][neighbor_y] != grid[x][y]:
                perimeter += 1

    return perimeter


def calculate_total_price(grid):
    """Calculates the total price for fencing all regions in the grid."""
    visited = set()
    total_price = 0

    for x in range(len(grid)):
        for y in range(len(grid)):
            if (x, y) not in visited:
                region_cells = explore_region(grid, x, y, visited)
                region_area = len(region_cells)
                region_perimeter = calculate_perimeter(grid, region_cells)
                total_price += region_area * region_perimeter

    return total_price


def main():  # NOQA: D103
    input_file = 'input.txt'
    grid = load_grid(input_file)
    result = calculate_total_price(grid)
    print(f'Total price of fencing all regions: {result}')


if __name__ == '__main__':
    main()
