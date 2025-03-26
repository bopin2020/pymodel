from core.lexer import *

class Token():
    def __init__(self,data,type : TokenType):
        self.str = data
        self.type = type

    def __repr__(self):
        return f'{self.type.name}  {self.str}'

class Express():
    def __init__(self):
        pass