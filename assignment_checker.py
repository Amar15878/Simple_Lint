import re
from enum import Enum

class BlockType(Enum):
    # Represents the type of block in SystemVerilog
    # sequential, combinational, continuous, or unknown
    SEQUENTIAL = 'sequential'
    COMBINATIONAL = 'combinational'
    CONTINUOUS = 'continuous'
    UNKNOWN = 'unknown' # Represents an unknown block type, e.g., not an always block or assign statement cannot be classified.

class AssignmentType(Enum):
    # Represents the type of assignment in Verilog
    # blocking or non-blocking
    BLOCKING = '='
    NON_BLOCKING = '<='

TRANSCRIPT_FILE = "transcript.txt"

def classify_always_block(header_line):
    # Classify the type of always block based on the header line
    # Check for posedge/negedge first, then check for combinational style
    if re.search(r'@(.*?posedge|negedge)', header_line):
        return BlockType.SEQUENTIAL
    # Then check for combinational style
    elif re.search(r'always_comb|@\(\*\)', header_line):
        return BlockType.COMBINATIONAL
    elif re.search(r'always\s*@\([^)]*\)', header_line):
        return BlockType.COMBINATIONAL
    else:
        return BlockType.UNKNOWN

###################### BLOCK EXTRACTION FUNCTION #####################
# This function extracts blocks of code from the lines of a Verilog file
def extract_blocks(lines):
    # Extract blocks of code from the lines of a Verilog file
    # Returns a list of tuples (block_type, lines, start_line)
    blocks = []
    current_block = []
    block_type = None
    inside_always = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^assign\s', stripped):
            blocks.append((BlockType.CONTINUOUS, [line], idx+1))
            continue

        if 'always' in stripped:
            if inside_always:
                blocks.append((block_type, current_block, start_line))
                current_block = []
            block_type = classify_always_block(stripped)
            inside_always = True
            start_line = idx + 1
            current_block = [line]

            if not re.search(r'begin', stripped):
                if idx + 1 < len(lines):
                    next_line = lines[idx + 1]
                    current_block.append(next_line)
                    blocks.append((block_type, current_block, start_line))
                    inside_always = False
        elif inside_always:
            current_block.append(line)
            if re.search(r'end\s*$', stripped):
                blocks.append((block_type, current_block, start_line))
                inside_always = False
                current_block = []

    return blocks


##################### ANALYSIS FUNCTION #####################
# This function analyzes the extracted blocks for assignment issues
def analyze_blocks(blocks):
    issues = []
    for block_type, lines, start_line in blocks:
        for offset, line in enumerate(lines):
            line_no = start_line + offset
            for match in re.finditer(r'(\w[\w\[\]\.]*?)\s*(<=|=)', line):
                signal, operator = match.groups()
                char_no = match.start(2) + 1
                assignment_type = AssignmentType(operator)

                if block_type == BlockType.SEQUENTIAL and assignment_type == AssignmentType.BLOCKING:
                    # check for blocking assignment in sequential block
                    issues.append((line_no, char_no, 'Incorrect use of blocking assignment (=)'))
                elif block_type == BlockType.COMBINATIONAL and assignment_type == AssignmentType.NON_BLOCKING:
                    # check for non-blocking assignment in combinational block
                    issues.append((line_no, char_no, 'Incorrect use of non-blocking assignment (<=)'))
                elif block_type == BlockType.CONTINUOUS and assignment_type == AssignmentType.NON_BLOCKING:
                    # check for non-blocking assignment in continuous block
                    issues.append((line_no, char_no, 'Incorrect use of non-blocking assignment (<=)'))

    return issues

##################### TRANSCRIPT WRITING FUNCTION #####################
# This function writes the issues found to a transcript file
def write_transcript(issues):
    # Write the issues found to a transcript file
    with open(TRANSCRIPT_FILE, 'w') as f:
        for line, char, msg in sorted(issues):
            f.write(f"Line {line}, Char {char}: {msg}\n")
    print(f"Transcript written to {TRANSCRIPT_FILE}")

##################### MAIN FUNCTION #####################
# This function reads a Verilog file, extracts blocks, analyzes them for issues,
def main(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    blocks = extract_blocks(lines)
    issues = analyze_blocks(blocks)
    write_transcript(issues)


##################### MAIN FUNCTION #####################
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python assignment_checker.py <file.sv>")
    else:
        main(sys.argv[1])