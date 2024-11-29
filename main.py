from lexer import Lexer, LexicalError
from parser import Parser, SyntaxError
from ast_visualizer import ASTVisualizer
from grammar import GRAMMAR_RULES

def print_phase_header(title: str):
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50 + "\n")

def print_grammar_rules():
    print_phase_header("Grammar Rules")
    print("Keywords:", ", ".join(GRAMMAR_RULES['keywords']))
    print("Operators:", ", ".join(GRAMMAR_RULES['operators']))
    print("Delimiters:", ", ".join(GRAMMAR_RULES['delimiters']))
    print("\nFor full grammar specification, see grammar.py")

def run_compiler(source_code: str):
    errors = []  # List to collect all errors
    tokens = []
    ast = []
    
    # Lexical Analysis
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
    except LexicalError as e:
        errors.append(f"Lexical Error: {e.message} at line {e.line}")
    
    # Continue with Syntax Analysis even if there are lexical errors
    if tokens:  # Only need tokens to proceed
        try:
            parser = Parser(tokens)
            ast = parser.parse()
        except SyntaxError as e:
            errors.append(f"Syntax Error: {e.message} at line {e.line}")
        except Exception as e:
            # Handle multiple errors
            for error in str(e).split('\n'):
                errors.append(error)

    # Symbol Table Generation
    symbol_table = {}
    try:
        for token in tokens:
            if token.type in ['IDENTIFIER', 'FUNCTION', 'VARIABLE']:
                symbol_table[token.value] = {
                    'type': token.type,
                    'line': token.line,
                    'column': token.column
                }
    except Exception as e:
        errors.append(f"Symbol Table Error: {str(e)}")

    # If there are any errors, only print errors
    if errors:
        for i, error in enumerate(errors, 1):
            print(f"Error {i}: {error}")
        print("\nCompilation failed.\n")
        return

    # If no errors, proceed with normal output
    print_grammar_rules()
    
    # Lexical Analysis Output
    print_phase_header("Lexical Analysis")
    print("Tokens:")
    for token in tokens:
        print(f"  {token} at line {token.line}, column {token.column}")

    # Syntax Analysis and AST Output
    print_phase_header("Syntax Analysis")
    print("Abstract Syntax Tree: \n")
    visualizer = ASTVisualizer()
    for node in ast:
        print(visualizer.visit(node))
        print()

    # Symbol Table Output
    print_phase_header("Symbol Table")
    if not symbol_table:
        print("No symbols found in the program.")
    else:
        print("Identifier | Type | Line | Column")
        print("-" * 40)
        for name, info in symbol_table.items():
            print(f"{name:<10} | {info['type']:<4} | {info['line']:<4} | {info['column']}")

    print("\nCompilation completed successfully.\n")

def main():
    # Read source code from files
    try:
        with open('test_valid.txt', 'r') as f:
            valid_program = f.read()
        with open('test_invalid.txt', 'r') as f:
            invalid_program = f.read()
        with open('test_invalid2.txt', 'r') as f:
            invalid_program2 = f.read()
    except FileNotFoundError as e:
        print(f"Error: Could not find test files - {str(e)}")
        return

    print("\nTesting valid program:")
    print("-" * 50)
    print(valid_program)
    print("-" * 50)
    run_compiler(valid_program)

    print("\nTesting invalid program 1:")
    print("-" * 50)
    print(invalid_program)
    print("-" * 50)
    run_compiler(invalid_program)

    print("\nTesting invalid program 2:")
    print("-" * 50)
    print(invalid_program2)
    print("-" * 50)
    run_compiler(invalid_program2)   
if __name__ == "__main__":
    main()