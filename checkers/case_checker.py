import re

def check_missing_default_case(filepath):
    """
    Checks for missing 'default' case in SystemVerilog 'case' statements.
    Returns a list of issues: (line_no, char_no, message)
    """
    issues = []
    with open(filepath, 'r') as file:
        lines = file.readlines()

    inside_case = False
    case_start_line = 0
    has_default = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^case\b', stripped):
            inside_case = True
            case_start_line = idx + 1
            has_default = False
        elif inside_case:
            if re.match(r'^default\b', stripped):
                has_default = True
            if re.match(r'^endcase\b', stripped):
                if not has_default:
                    issues.append((case_start_line, 1, "Missing 'default' case in case statement.\n\t---> HINT: Add a 'default' branch to your case statement.\n"))
                inside_case = False
    return issues
