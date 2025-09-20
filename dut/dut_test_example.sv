// Some Random Verilog code with various assignment issues
// This code is for testing the assignment_checker.py script
module test(input clk, rst_n, input enable, output reg ready, input [7:0] data_in, output reg [7:0] output_data);
    always @(posedge clk or negedge rst_n) begin
      if (!rst_n) begin
        count <= 0;
      end else begin
        count <= count + 1;
      end
    end

    // --- CASE STATEMENT TESTS ---
    // Correct case statement (has default)
    always_comb begin
      case (data_in)
        8'h00: output_data = 0;
        8'hFF: output_data = 255;
        default: output_data = 42;
      endcase
    end

    // Incorrect case statement (missing default)
    always_comb begin
      case (data_in)
        8'h01: output_data = 1;
        8'h02: output_data = 2;
      endcase
    end

    // --- GENVAR USAGE TESTS ---
    // Correct genvar usage
    genvar i;
    generate
      for (i = 0; i < 4; i = i + 1) begin : gen_block_correct
        wire [3:0] temp = i;
      end
    endgenerate

    // Incorrect genvar usage (missing genvar declaration)
    generate
      for (j = 0; j < 4; j = j + 1) begin : gen_block_incorrect
        wire [3:0] temp2 = j;
      end
    endgenerate

    // Incorrect
    always @(posedge clk) begin
      data = data + 1; // Should be <=
    end

    // Correct assign statement
    assign valid = enable & ready;

    // Incorrect assign statement
    assign output_data <= data_in; 

    always_comb begin
      if (reset) begin
        output_data <= 0; // Incorrect
      end else begin
        output_data <= data_in; // Incorrect
      end
    end
endmodule