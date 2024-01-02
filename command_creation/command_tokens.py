from typing import Protocol

class CommandToken(Protocol):
    def get_string(self) -> str:
        ...

class CommandConstant:
    def __init__(self, name : str, value : str = None):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.name == other.name

class CommandVariable:
    def __init__(self, name : str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

class CommandConstToken:
    def __init__(self, const : CommandConstant, declaration=True):
        self.const = const
        self.declaration = declaration

    def get_string(self) -> str:
        s = self.const.name
        if self.declaration:
            s += "=" + self.const.value
            
        return s
    
    def non_declared_shallow_copy(self):
        return CommandConstToken(self.const, False)

    def __eq__(self, other):
        return self.const == other.const
    
class CommandVarToken:
    def __init__(self, var : CommandVariable):
        self.var = var

    def get_string(self) -> str:
        return self.var.name
    
    def __eq__(self, other):
        return self.var == other.var
    
class CommandStringToken:
    def __init__(self, string : str):
        self.string = string

    def get_string(self) -> str:
        return self.string
    
    def __eq__(self, other):
        return self.string == other.string