from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ASTNode:
    def __str__(self):
        return self.__class__.__name__

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

@dataclass
class Number(ASTNode):
    value: int

    def __str__(self):
        return str(self.value)

@dataclass
class Variable(ASTNode):
    name: str

    def __str__(self):
        return self.name

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode

    def __str__(self):
        return f"{self.name} = {self.value}"

@dataclass
class Display(ASTNode):
    expression: ASTNode

    def __str__(self):
        return f"display({self.expression})"

@dataclass
class If(ASTNode):
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]]

    def __str__(self):
        result = f"if ({self.condition}) {{ {', '.join(str(stmt) for stmt in self.then_block)} }}"
        if self.else_block:
            result += f" else {{ {', '.join(str(stmt) for stmt in self.else_block)} }}"
        return result