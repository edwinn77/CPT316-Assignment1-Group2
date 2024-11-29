class ASTVisualizer:
    def __init__(self):
        self.indent = 0
        self.current_buffer = []
        self.next_buffer = []
        
    def visit(self, node) -> str:
        method_name = f'visit_{node.__class__.__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
        
    def generic_visit(self, node):
        return str(node)
        
    def indent_str(self) -> str:
        return '  ' * self.indent
        
    def visit_list(self, nodes) -> str:
        self.indent += 1
        result = '\n'.join(f"{self.indent_str()}└─ {self.visit(node)}" for node in nodes)
        self.indent -= 1
        return result
        
    def visit_BinaryOp(self, node):
        return f"BinaryOp: {node.operator}\n{self.indent_str()}  ├─ Left: {self.visit(node.left)}\n{self.indent_str()}  └─ Right: {self.visit(node.right)}"
        
    def visit_Number(self, node):
        return f"Number: {node.value}"
        
    def visit_Variable(self, node):
        return f"Variable: {node.name}"
        
    def visit_Assignment(self, node):
        return f"Assignment:\n{self.indent_str()}  ├─ Name: {node.name}\n{self.indent_str()}  └─ Value: {self.visit(node.value)}"
        
    def visit_Display(self, node):
        return f"Display:\n{self.indent_str()}  └─ Expression: {self.visit(node.expression)}"
        
    def visit_If(self, node):
        result = [f"If:\n{self.indent_str()}  ├─ Condition: {self.visit(node.condition)}"]
        
        self.indent += 2
        result.append(f"{self.indent_str()}├─ Then:")
        result.append(self.visit_list(node.then_block))
        
        if node.else_block:
            result.append(f"{self.indent_str()}└─ Else:")
            result.append(self.visit_list(node.else_block))
        self.indent -= 2
        
        return '\n'.join(result)
        
    def render(self, ast):
        # Prepare the next buffer
        self.next_buffer = [self.visit(node) for node in ast]
        
        # Swap buffers
        self.current_buffer, self.next_buffer = self.next_buffer, self.current_buffer
        
        # Display the current buffer
        print('\n'.join(self.current_buffer))