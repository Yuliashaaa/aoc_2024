from operator import xor
from pathlib import Path

input_file = Path('input.txt')
lines = list(map(int, input_file.read_text().strip().split('\n')))


def mix(a, b):  # NOQA: D103
    return xor(a, b)


def prune(a):  # NOQA: D103
    return a % 16777216


def next_secret(x):  # NOQA: D103
    x = prune(mix(x, x * 64))
    x = prune(mix(x, x // 32))
    x = prune(mix(x, x * 2048))

    return x  # NOQA: RET504


def get_profit(seed):
    """Calculate all possible profit sequences for a given seed."""
    seq = [seed % 10]
    profit = {}
    x = seed

    for i in range(2000):
        x = next_secret(x)
        seq.append(x % 10)

        if i >= 3:  # NOQA: PLR2004
            changes = tuple(seq[j] - seq[j - 1] for j in range(i - 2, i + 2))
            if changes not in profit:
                profit[changes] = seq[i + 1]

    return profit


def get_total_profit(sequence):
    """Calculate total profit for a given change sequence."""
    total = 0

    for profit in profits:
        if sequence in profit:
            total += profit[sequence]

    return total


profits = [get_profit(seed) for seed in lines]
unique_sequences = set()

for profit in profits:
    unique_sequences.update(profit.keys())

max_bananas = 0

for sequence in unique_sequences:
    max_bananas = max(max_bananas, get_total_profit(sequence))

print(max_bananas)
