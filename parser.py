from typing import List, Optional
from lexer import Token
from ast_nodes import *
from symbol_table import SymbolTable

class SyntaxError(Exception):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"{message} at line {line}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.symbol_table = SymbolTable()
        self.errors = []

    def error(self, message: str):
        token = self.tokens[self.current]
        self.errors.append(SyntaxError(message, token.line))
        self.sync()

    def sync(self):
        """Skip tokens until we find a semicolon or block delimiter, or reach the end of tokens."""
        while self.peek() and self.peek().value not in [';', '}', 'NEWLINE']:
            self.advance()
        # Advance past the semicolon or closing brace if found
        if self.peek() and self.peek().value in [';', '}']:
            self.advance()

    def peek(self) -> Optional[Token]:
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def advance(self) -> Token:
        token = self.peek()
        self.current += 1
        return token

    def match(self, *types) -> bool:
        if self.peek() and self.peek().type in types:
            self.advance()
            return True
        return False

    def expect(self, type_: str, value: Optional[str] = None) -> Token:
        token = self.peek()
        if not token or token.type != type_ or (value and token.value != value):
            expected = value if value else type_
            self.error(f"Expected '{expected}'")
        self.advance()
        return token

    def parse(self) -> List[ASTNode]:
        statements = []
        while self.peek():
            try:
                stmt = self.statement()
                if stmt:
                    statements.append(stmt)
            except Exception as e:
                self.error(str(e))
        
        if self.errors:
            raise Exception("\n".join(str(err) for err in self.errors))
        return statements

    def statement(self) -> ASTNode:
        if self.match('DISPLAY'):
            return self.display_statement()
        elif self.match('IF'):
            return self.if_statement()
        elif self.peek().type == 'IDENTIFIER':
            return self.assignment()
        elif self.match('NEWLINE'):
            return None  # Ignore new lines
        self.error("Expected statement")

    def display_statement(self) -> Display:
        self.expect('DELIMITER', '(')
        expr = self.expression()
        self.expect('DELIMITER', ')')
        self.expect('DELIMITER', ',')
        return Display(expr)

    def if_statement(self) -> If:
        self.expect('DELIMITER', '(')
        condition = self.expression()
        self.expect('DELIMITER', ')')
        self.expect('DELIMITER', '{')

        then_block = []
        while self.peek() and self.peek().value != '}':
            then_block.append(self.statement())

        # Check for the closing brace of the if block
        if not self.match('DELIMITER', '}'):
            self.error("Expected '}' to close the if statement")

        else_block = None
        if self.match('ELSE'):
            self.expect('DELIMITER', '{')
            else_block = []
            while self.peek() and self.peek().value != '}':
                else_block.append(self.statement())
            self.expect('DELIMITER', '}')

        return If(condition, then_block, else_block)

    def assignment(self) -> Assignment:
        name = self.advance().value
        self.expect('ASSIGN')
        value = self.expression()
        self.expect('DELIMITER', ',')
        self.symbol_table.define(name, value)
        return Assignment(name, value)

    def expression(self) -> ASTNode:
        left = self.arithmetic()
        
        while self.peek() and self.peek().value in ['>', '<', '>=', '<=', '==', '!=']:
            operator = self.advance().value
            right = self.arithmetic()
            left = BinaryOp(left, operator, right)
            
        return left

    def arithmetic(self) -> ASTNode:
        left = self.term()
        
        while self.peek() and self.peek().value in '+-':
            operator = self.advance().value
            right = self.term()
            left = BinaryOp(left, operator, right)
            
        return left

    def term(self) -> ASTNode:
        left = self.factor()
        
        while self.peek() and self.peek().value in '*/':
            operator = self.advance().value
            right = self.factor()
            left = BinaryOp(left, operator, right)
            
        return left

    def factor(self) -> ASTNode:
        token = self.peek()
        
        if self.match('NUMBER'):
            return Number(int(token.value))
        elif self.match('IDENTIFIER'):
            return Variable(token.value)
        elif self.match('DELIMITER') and token.value == '(':
            expr = self.expression()
            self.expect('DELIMITER', ')')
            return expr
            
        self.error("Expected expression")