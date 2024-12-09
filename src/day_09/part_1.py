from pathlib import Path


def part_a(puzzle_input: str) -> int:
    """Solves part 1 of the puzzle. Parses the input, sorts the blocks, and calculates the score."""
    problem = Blocks.parse(puzzle_input)
    problem.sort()
    return problem.score()


class Blocks:  # NOQA: D101
    def __init__(self, blocks: list[int | None]):  # NOQA: ANN204, D107
        self.blocks = blocks

    @staticmethod
    def parse(puzzle_input: str) -> 'Blocks':
        """Parses the input string into a Blocks object. Each block is represented by an ID or None for free space."""
        blocks = []
        id_counter = 0

        for idx, char in enumerate(puzzle_input.strip()):
            count = int(char)  # Convert char to an integer
            is_block = idx % 2 == 0
            item = id_counter if is_block else None

            blocks.extend([item] * count)
            id_counter += is_block

        return Blocks(blocks)

    def sort(self):
        """Sorts the blocks by moving file blocks to the leftmost available space."""
        while True:
            empty_idx = next((i for i, block in enumerate(self.blocks) if block is None), None)
            last_idx = next((i for i in range(len(self.blocks) - 1, -1, -1) if self.blocks[i] is not None), None)

            if last_idx is None or empty_idx is None or last_idx <= empty_idx:
                break

            # Swap the empty space with the last filled block
            self.blocks[empty_idx], self.blocks[last_idx] = self.blocks[last_idx], self.blocks[empty_idx]

    def score(self) -> int:
        """Calculates the score based on the positions and IDs of the blocks."""
        return sum(i * (block if block is not None else 0) for i, block in enumerate(self.blocks))


def read_input_file(file_path: str) -> str:
    """Reads the input data from a text file."""
    path = Path(file_path)
    with path.open() as file:
        return file.read().strip()


if __name__ == '__main__':
    input_data = read_input_file('input.txt')
    result = part_a(input_data)
    print(f'Part 1 result: {result}')
