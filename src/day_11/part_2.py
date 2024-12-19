from collections import Counter
from pathlib import Path


def parse_input(file_path: Path) -> list[int]:
    """Parse the input file into a list of integers representing the stones."""
    with file_path.open() as file:
        return list(map(int, file.read().strip().split()))


def evolve_stone_counts(stone_counts):
    """Evolves the stone counts by applying the transformation rules."""
    new_counts = Counter()

    for stone, count in stone_counts.items():
        if stone == 0:
            # Rule 1: 0 -> 1
            new_counts[1] += count
        elif len(str(stone)) % 2 == 0:
            # Rule 2: Split even-digit numbers
            digits = str(stone)
            mid = len(digits) // 2
            left = int(digits[:mid])
            right = int(digits[mid:])
            new_counts[left] += count
            new_counts[right] += count
        else:
            # Rule 3: Multiply by 2024
            new_counts[stone * 2024] += count

    return new_counts


def simulate_blinks_optimized(stones, blinks):
    """Simulates the blinking process for a given number of blinks."""
    stone_counts = Counter(stones)

    for _ in range(blinks):
        stone_counts = evolve_stone_counts(stone_counts)

    return sum(stone_counts.values())


if __name__ == '__main__':
    input_path = Path('input.txt')
    initial_stones = parse_input(input_path)

    total_stones = simulate_blinks_optimized(initial_stones, 75)
    print(f'Total stones after 75 blinks: {total_stones}')
