import os

def main():
    # Compile the .g4 grammar file
    grammar_file = "YAPL.g4"  # Replace with your own .g4 file
    compile_command = f"antlr4 -Dlanguage=Python3 {grammar_file}"
    os.system(compile_command)
    print("Grammar file compiled successfully.")

    # Parse the input file and generate the parse tree visualization
    input_file = "ejemplo.yapl"  # Replace with your own input file
    parse_tree_file = "parse_tree.png"
    parse_command = f"antlr4-parse YAPL.g4 program  -gui {input_file}"
    os.system(parse_command)
    print(f"Parse tree visualization saved as {parse_tree_file}.")

if __name__ == '__main__':
    main()
