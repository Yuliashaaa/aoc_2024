from pathlib import Path


def part_b(puzzle_input: str) -> int:
    """Solves part 2 of the puzzle. Parses the input, compacts the blocks, and calculates the score."""
    problem = Blocks.parse(puzzle_input)
    problem.compact()

    return problem.score()


def _update_free_ranges(free_ranges: list[tuple], start: int, used_length: int):  # NOQA: ANN202
    """Updates the free_ranges list after a range is used."""
    for i, (free_start, free_length) in enumerate(free_ranges):
        if free_start == start:
            if free_length > used_length:
                free_ranges[i] = (free_start + used_length, free_length - used_length)
            else:
                free_ranges.pop(i)
            break


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

    def compact(self):
        """Compacts the blocks by moving whole files to the leftmost available span of free space that can fit them.

        Processes files in order of decreasing file ID.
        """
        file_positions = {}

        for idx, block in enumerate(self.blocks):
            if block is not None:
                if block not in file_positions:
                    file_positions[block] = []
                file_positions[block].append(idx)

        free_ranges = self._find_free_ranges()

        for file_id in sorted(file_positions.keys(), reverse=True):
            file_indices = file_positions[file_id]
            file_length = len(file_indices)

            # Try to find a free range that can fit the file
            for start, length in free_ranges:
                if length >= file_length and start < file_indices[0]:
                    # Move the file to this free range
                    for j in range(file_length):
                        self.blocks[start + j] = file_id
                        self.blocks[file_indices[j]] = None

                    # Update free_ranges
                    _update_free_ranges(free_ranges, start, file_length)
                    break

    def _find_free_ranges(self) -> list[tuple]:
        """Identifies contiguous free space ranges in the block list."""
        free_ranges = []
        start = None

        for i, block in enumerate(self.blocks):
            if block is None:
                if start is None:
                    start = i
            elif start is not None:
                free_ranges.append((start, i - start))
                start = None

        if start is not None:
            free_ranges.append((start, len(self.blocks) - start))

        return free_ranges

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
    result = part_b(input_data)
    print(f'Part 2 result: {result}')
