from pathlib import Path


def parse_input(file_path: Path) -> list[int]:
    """Parse the input file into a list of integers representing the stones."""
    with file_path.open() as file:
        return list(map(int, file.read().strip().split()))


def evolve_stones(stones: list[int]) -> list[int]:
    """Evolve the stones based on the rules provided."""
    new_stones = []

    for stone in stones:
        if stone == 0:
            # Rule 1: Stone engraved with 0 becomes 1
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            # Rule 2: Split stone with even number of digits
            mid = len(str(stone)) // 2
            left = int(str(stone)[:mid])
            right = int(str(stone)[mid:])
            new_stones.extend([left, right])
        else:
            # Rule 3: Multiply by 2024
            new_stones.append(stone * 2024)

    return new_stones


def simulate_blinks(stones: list[int], blinks: int) -> int:
    """Simulate the stones evolving over a given number of blinks."""
    for _ in range(blinks):
        stones = evolve_stones(stones)

    return len(stones)


def main():
    """Main function to calculate the result for the given input file and blink count."""
    input_file = Path('input.txt')
    stones = parse_input(input_file)
    blinks = 25
    result = simulate_blinks(stones, blinks)
    print(f'Number of stones after {blinks} blinks: {result}')


if __name__ == '__main__':
    main()
