# Simple Lint Script
*This is a simple python script to check systemverilog file (mainly dut) for potential assignment misuse.*

Feature : 
+ Detects assignment misuse (blocking vs. non-blocking) in always and assign blocks
+ Checks for missing 'default' in case statements
+ Checks for improper genvar usage in generate loops
+ Reports violations with line and character precision
+ Generates structured, human-readable reports for fast debugging
+ Modular checker design for easy extensibility


# Run
+ ..\Simple_Lint> python -m Script.simple_lint dut/dut_test_example.v
