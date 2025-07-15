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