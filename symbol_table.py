class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, value):
        self.symbols[name] = value

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        raise Exception(f"Undefined variable: {name}")

    def __str__(self):
        return str(self.symbols) 