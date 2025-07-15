*This is a simple python script to check systemverilog file (mainly dut) for potential assignment misuse.*

Feature : 

-> Able to identify misuse of blocking or non-blocking assignemnt in blocks (be it procedural, combinational or other).

-> For now supports identification of always_comb and always_ff keyword for the lint check (NOTE : not fool-proof yet).

