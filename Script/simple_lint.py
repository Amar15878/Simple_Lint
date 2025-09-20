from checkers.blocking_nonblocking_checker import check_blocking_nonblocking
from checkers.case_checker import check_missing_default_case
from checkers.genvar_checker import check_improper_genvar_usage

import datetime
REPORT_FILE = "transcript.txt"

# Map checkers to rule names for report clarity
RULE_MAP = {
    'check_blocking_nonblocking': 'Blocking/Non-blocking Assignment',
    'check_missing_default_case': 'Case Statement',
    'check_improper_genvar_usage': 'Genvar Usage',
}

def write_structured_report(issues, filename, checked_file):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'w') as f:
        f.write("Simple_Lint Violation Report\n")
        f.write(f"File: {checked_file}\n")
        f.write(f"Date: {now}\n")
        f.write(f"Total Lint Violations: {len(issues)}\n\n")
        f.write("-"*80 + "\n")
        for issue in sorted(issues, key=lambda x: (x['line'], x['char'])):
            f.write(f"Line {issue['line']}, Char {issue['char']} | [{issue['rule']}] | WARNING\n")
            f.write(issue['msg'])
            if not issue['msg'].endswith('\n'):
                f.write('\n')
            f.write("\n")
        f.write("-"*80 + "\n")
    print(f"Structured report written to {filename}")

def main(filepath):
    # Call all checkers and aggregate issues with rule names
    issues = []
    for checker, rule in [
        (check_blocking_nonblocking, RULE_MAP['check_blocking_nonblocking']),
        (check_missing_default_case, RULE_MAP['check_missing_default_case']),
        (check_improper_genvar_usage, RULE_MAP['check_improper_genvar_usage']),
    ]:
        for result in checker(filepath):
            # result: (line, char, msg)
            issues.append({
                'line': result[0],
                'char': result[1],
                'msg': result[2],
                'rule': rule
            })
    write_structured_report(issues, REPORT_FILE, filepath)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python simple_lint.py <file.sv>")
    else:
        main(sys.argv[1])
