from pathlib import Path


def parse_input(file_path):
    """Reads and parses the input file into a list of reports (lists of integers)."""
    with Path(file_path).open() as f:
        return [list(map(int, line.split())) for line in f]


def is_safe_report(report):
    """Checks if a report is safe based on the given rules."""
    is_increasing = all(report[i] < report[i + 1] for i in range(len(report) - 1))
    is_decreasing = all(report[i] > report[i + 1] for i in range(len(report) - 1))
    valid_differences = all(1 <= abs(report[i] - report[i + 1]) <= 3 for i in range(len(report) - 1))  # NOQA: PLR2004

    return (is_increasing or is_decreasing) and valid_differences


def count_safe_reports(data):
    """Counts the number of safe reports from the data."""
    safe_count = 0
    for report in data:
        if is_safe_report(report):
            safe_count += 1

    return safe_count


if __name__ == '__main__':
    input_file = 'input.txt'
    reports = parse_input(input_file)
    safe_reports_count = count_safe_reports(reports)
    print(f'Number of safe reports: {safe_reports_count}')
