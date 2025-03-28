from core.header import *

class ProcessModel:
    def __init__(self):
        self.modules = range(0,10)
        self.pid = 0
        self.name = 'cmd.exe'

    def get_modules(self):
        return 
    
    def get_pid(self):
        return self.pid
    
    def get_name(self):
        return self.name

    def set_name(self,name):
        self.name = name
        return OperateResult.Success

    def __repr__(self):
        return f'modules\nget_modules()'
    

class MemoryModel:
    def __init__(self):
        self.data = random.randbytes(0x1000)

    def get_bytes(self,addr,off):
        if isinstance(off,str):
            if off.startswith('0x'):
                off = int(off,16)
            else:
                off = int(off)
        return self.data[:off]
    
    def test(self,id):
        return id

    def __repr__(self):
        return f'data\nget_bytes()\ntest()'
    
class ThreadModel:
    def __init__(self):
        self.id = 0

    def get_tid(self,v1,v2):
        return self.id

class LexerError(Exception):
    """Lexer parse exception
    """
    def __init__(self,type,message,error_code):
        super().__init__(message)
        self.type = type
        self.error_code = error_code

    def __str__(self):
        return super().__str__()