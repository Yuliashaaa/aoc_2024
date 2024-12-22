from operator import xor
from pathlib import Path


def mix(a, b):
    """Perform a bitwise XOR operation to mix two numbers."""
    return xor(a, b)


def prune(a):
    """Prune a number by taking it modulo 16777216."""
    return a % 16777216


def next_secret(x):
    """Generate the next secret number in the sequence."""
    x = prune(mix(x, x * 64))
    x = prune(mix(x, x // 32))
    x = prune(mix(x, x * 2048))

    return x  # NOQA: RET504


def get_idx(seed, idx):
    """Get the secret number at the specified index in the sequence."""
    x = seed

    for _ in range(idx):
        x = next_secret(x)

    return x


def main():  # NOQA: D103
    input_file = Path('input.txt')
    with input_file.open() as fin:
        lines = list(map(int, fin.read().strip().split('\n')))

    results = [get_idx(x, 2000) for x in lines]
    total_sum = sum(results)
    print('2000th secret numbers:', results)
    print('Sum of 2000th secret numbers:', total_sum)


if __name__ == '__main__':
    main()
