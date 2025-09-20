import re

def check_improper_genvar_usage(filepath):
    """
    Checks for improper usage of 'genvar' in SystemVerilog generate loops.
    Returns a list of issues: (line_no, char_no, message)
    """
    issues = []
    with open(filepath, 'r') as file:
        lines = file.readlines()

    genvars = set()
    for idx, line in enumerate(lines):
        # Find genvar declarations
        for match in re.finditer(r'genvar\s+(\w+)', line):
            genvars.add(match.group(1))

    for idx, line in enumerate(lines):
        # Find for-loops in generate blocks
        for match in re.finditer(r'for\s*\(([^;]+);([^;]+);([^\)]+)\)', line):
            init, cond, inc = match.groups()
            # Try to extract loop variable
            loop_var_match = re.search(r'(\w+)\s*=.*', init)
            if loop_var_match:
                loop_var = loop_var_match.group(1)
                if loop_var not in genvars:
                    char_no = match.start(1) + 1
                    issues.append((idx+1, char_no, f"Loop variable '{loop_var}' in generate for-loop is not declared as genvar.\n\t---> HINT: Declare '{loop_var}' as a genvar before using in generate for-loops.\n"))
    return issues
