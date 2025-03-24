from header import *

class ProcessModel:
    def __init__(self):
        self.modules = []

    def get_modules(self):
        return self.modules

class MemoryModel:
    def __init__(self):
        self.data = random.randbytes(0x1000)

    def get_bytes(self,addr,off):
        return self.data[:off]
    
    def test(self,id):
        pass