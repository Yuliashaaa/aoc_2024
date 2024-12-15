from pathlib import Path


def parse_input(file_path):
    """Parses the input file into a list of positions and velocities."""
    robots = []
    file_path = Path(file_path)

    with file_path.open() as file:
        for line in file:
            if line.strip():
                parts = line.split()
                position = tuple(map(int, parts[0][2:].split(',')))
                velocity = tuple(map(int, parts[1][2:].split(',')))
                robots.append((position, velocity))

    return robots


def simulate_motion(robots, width, height, time_steps):
    """Simulates the robots' motion over a given number of time steps."""
    final_positions = []

    for position, velocity in robots:
        x = (position[0] + velocity[0] * time_steps) % width
        y = (position[1] + velocity[1] * time_steps) % height
        final_positions.append((x, y))

    return final_positions


def calculate_quadrants(positions, width, height):
    """Calculates the number of robots in each quadrant."""
    mid_x = width // 2
    mid_y = height // 2
    quadrants = [0, 0, 0, 0]  # Quadrant 1, 2, 3, 4

    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue  # Skip robots exactly in the middle
        if x < mid_x and y < mid_y:
            quadrants[0] += 1  # Top-left (Quadrant 1)
        elif x >= mid_x and y < mid_y:
            quadrants[1] += 1  # Top-right (Quadrant 2)
        elif x < mid_x and y >= mid_y:
            quadrants[2] += 1  # Bottom-left (Quadrant 3)
        elif x >= mid_x and y >= mid_y:
            quadrants[3] += 1  # Bottom-right (Quadrant 4)

    return quadrants


def calculate_safety_factor(quadrants):
    """Calculates the safety factor as the product of quadrant counts."""
    factor = 1

    for count in quadrants:
        factor *= count

    return factor


def main():  # NOQA: D103
    input_file = 'input.txt'
    width, height = 101, 103  # Dimensions of the space
    time_steps = 100  # Time steps to simulate

    robots = parse_input(input_file)
    final_positions = simulate_motion(robots, width, height, time_steps)
    quadrants = calculate_quadrants(final_positions, width, height)
    safety_factor = calculate_safety_factor(quadrants)
    print(f'Safety Factor: {safety_factor}')


if __name__ == '__main__':
    main()
