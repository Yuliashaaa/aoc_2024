from src.day_02.part_1 import is_safe_report, parse_input


def can_be_safe_with_dampener(report):
    """Checks if a report can be made safe by removing one level."""
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]
        if is_safe_report(modified_report):
            return True

    return False


def count_safe_reports_with_dampener(data):
    """Counts the number of safe reports, considering the Problem Dampener."""
    safe_count = 0
    for report in data:
        if is_safe_report(report) or can_be_safe_with_dampener(report):
            safe_count += 1

    return safe_count


if __name__ == '__main__':
    input_file = 'input.txt'
    reports = parse_input(input_file)

    safe_reports_count = count_safe_reports_with_dampener(reports)
    print(f'Number of safe reports (with Problem Dampener): {safe_reports_count}')
