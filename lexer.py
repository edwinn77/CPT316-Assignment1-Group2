from dataclasses import dataclass
from typing import List, Optional
from grammar import GRAMMAR_RULES

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return f"Token({self.type}, '{self.value}')"

class LexicalError(Exception):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"{message} at line {line}")

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None
        self.line = 1
        self.column = 1

    def error(self, message: str):
        raise LexicalError(message, self.line)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1

    def peek_next(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def get_number(self) -> Token:
        result = ''
        token_column = self.column
        
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
            
        if self.current_char and self.current_char.isalpha():
            self.error("Invalid identifier: cannot start with a number")
            
        return Token('NUMBER', result, self.line, token_column)

    def get_identifier(self) -> Token:
        result = ''
        token_column = self.column
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        if result in GRAMMAR_RULES['keywords']:
            return Token(result.upper(), result, self.line, token_column)
        return Token('IDENTIFIER', result, self.line, token_column)

    def tokenize(self) -> List[Token]:
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char == '#':
                self.skip_comment()
                continue
                
            if self.current_char.isdigit():
                tokens.append(self.get_number())
                continue
                
            if self.current_char.isalpha():
                tokens.append(self.get_identifier())
                continue
                
            if self.current_char == '=':
                token_column = self.column
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('OPERATOR', '==', self.line, token_column))
                    self.advance()
                else:
                    tokens.append(Token('ASSIGN', '=', self.line, token_column))
                continue
                
            if self.current_char == '>':
                token_column = self.column
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('OPERATOR', '>=', self.line, token_column))
                    self.advance()
                else:
                    tokens.append(Token('OPERATOR', '>', self.line, token_column))
                continue
                
            if self.current_char == '<':
                token_column = self.column
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('OPERATOR', '<=', self.line, token_column))
                    self.advance()
                else:
                    tokens.append(Token('OPERATOR', '<', self.line, token_column))
                continue
                
            if self.current_char in '(){},':
                tokens.append(Token('DELIMITER', self.current_char, self.line, self.column))
                self.advance()
                continue
                
            if self.current_char in '+-*/':
                tokens.append(Token('OPERATOR', self.current_char, self.line, self.column))
                self.advance()
                continue
                
            if self.current_char == '\n':
                tokens.append(Token('NEWLINE', '\\n', self.line, self.column))
                self.advance()
                continue
                
            self.error(f"Invalid character '{self.current_char}'")
            
        return tokens