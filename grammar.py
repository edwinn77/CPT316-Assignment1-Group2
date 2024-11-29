"""
MiniLang Grammar Specification

Program ::= Statement*

Statement ::= AssignmentStmt
            | IfStmt
            | DisplayStmt

AssignmentStmt ::= Identifier '=' Expression ';'

IfStmt ::= 'if' '(' Expression ')' '{' Statement* '}' 
           ['else' '{' Statement* '}']

DisplayStmt ::= 'display' '(' Expression ')' ';'

Expression ::= ArithExpr
             | ArithExpr RelOp ArithExpr

ArithExpr ::= Term
            | ArithExpr ('+' | '-') Term

Term ::= Factor
       | Term ('*' | '/') Factor

Factor ::= Number
         | Identifier
         | '(' Expression ')'

RelOp ::= '>' | '<' | '>=' | '<=' | '==' | '!='

Identifier ::= Letter (Letter | Digit)*
Number ::= Digit+
Letter ::= [a-zA-Z]
Digit ::= [0-9]
"""

GRAMMAR_RULES = {
    'keywords': ['if', 'else', 'display'],
    'operators': ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!='],
    'delimiters': ['(', ')', '{', '}', ',', '='],
}