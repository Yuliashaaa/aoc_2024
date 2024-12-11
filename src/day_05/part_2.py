from collections import defaultdict, deque
from pathlib import Path


def parse_input(file_path: Path) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """Parse the input file into rules and updates."""
    with file_path.open() as f:
        sections = f.read().strip().split('\n\n')

    rules = []
    for line in sections[0].splitlines():
        x, y = map(int, line.split('|'))
        rules.append((x, y))

    updates = [list(map(int, line.split(','))) for line in sections[1].splitlines()]

    return rules, updates


def build_dependency_graph(rules: list[tuple[int, int]]) -> dict[int, set[int]]:
    """Build a dependency graph from the rules."""
    graph = defaultdict(set)

    for x, y in rules:
        graph[x].add(y)

    return graph


def is_correct_order(update: list[int], graph: dict[int, set[int]]) -> bool:
    """Check if a given update is in the correct order."""
    position = {page: i for i, page in enumerate(update)}

    for x in update:
        if x in graph:
            for y in graph[x]:
                if y in position and position[x] > position[y]:
                    return False

    return True


def topological_sort(update: list[int], graph: dict[int, set[int]]) -> list[int]:
    """Reorder a given update using topological sort."""
    # Filter the dependency graph to include only the pages in the current update
    in_degrees = {page: 0 for page in update}
    adj_list = defaultdict(list)

    for x in update:
        if x in graph:
            for y in graph[x]:
                if y in update:
                    adj_list[x].append(y)
                    in_degrees[y] += 1

    # Perform topological sort
    queue = deque([node for node in update if in_degrees[node] == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)

        for neighbor in adj_list[current]:
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order


def calculate_incorrect_middle_sum(updates: list[list[int]], graph: dict[int, set[int]]) -> int:
    """Calculate the sum of middle page numbers of incorrectly ordered updates after correcting them."""
    middle_sum = 0

    for update in updates:
        if not is_correct_order(update, graph):
            corrected = topological_sort(update, graph)
            middle_sum += corrected[len(corrected) // 2]

    return middle_sum


def main(file_path: str) -> int:
    """Main function to calculate the result for Part Two."""
    rules, updates = parse_input(Path(file_path))
    graph = build_dependency_graph(rules)

    return calculate_incorrect_middle_sum(updates, graph)


if __name__ == '__main__':
    input_file = 'input.txt'
    result = main(input_file)
    print(f'Sum of Middle Page Numbers (Incorrect Updates): {result}')
