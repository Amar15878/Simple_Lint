import re
from enum import Enum

class BlockType(Enum):
    SEQUENTIAL = 'sequential'
    COMBINATIONAL = 'combinational'
    CONTINUOUS = 'continuous'
    UNKNOWN = 'unknown'

class AssignmentType(Enum):
    BLOCKING = '='
    NON_BLOCKING = '<='

def classify_always_block(header_line):
    if re.search(r'@(.*?posedge|negedge)', header_line):
        return BlockType.SEQUENTIAL
    elif re.search(r'always_comb|@\(\*\)', header_line):
        return BlockType.COMBINATIONAL
    elif re.search(r'always\s*@\([^)]*\)', header_line):
        return BlockType.COMBINATIONAL
    else:
        return BlockType.UNKNOWN

def extract_blocks(lines):
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
                    issues.append((line_no, char_no, 'Incorrect use of blocking assignment (=) \n\t---> HINT: Try Using non-blocking assignment (<=) instead.\n'))
                elif block_type == BlockType.COMBINATIONAL and assignment_type == AssignmentType.NON_BLOCKING:
                    issues.append((line_no, char_no, 'Incorrect use of non-blocking assignment (<=) \n\t---> HINT: Try Using blocking assignment (=) instead.\n'))
                elif block_type == BlockType.CONTINUOUS and assignment_type == AssignmentType.NON_BLOCKING:
                    issues.append((line_no, char_no, 'Incorrect use of non-blocking assignment (<=) \n\t---> HINT: Try Using blocking assignment (=) instead.\n'))
    return issues

def check_blocking_nonblocking(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    blocks = extract_blocks(lines)
    issues = analyze_blocks(blocks)
    return issues
