from core.expresstoken import *
from core.lexer import *

class MethodExpress(ConsoleLogable):
    """Parse call method expression such as process.callmethod()
    convert it into ast after tokenizer
                obj
            prcess  callmethod
    """
    def __init__(self):
        self.expr = {
            "methodname":"",
            "methodparas":[

            ]
        }

    def parse(self,input):
        state = MethodParseState.Init
        accum = ''
        off = 0
        self.expr['methodname'] = ''
        self.expr['methodparas'] = []
        while(off <= len(input)):
            cr = input[off] if off < len(input)-0 else ''
            nr = input[off + 1]  if off < len(input)-1 else ''
            nnr = input[off + 2]  if off < len(input)-2 else ''
            match state:                
                case MethodParseState.Init:
                    if cr not in symbols:
                        accum += cr
                    else:
                        accum = accum.strip()
                        self.expr['methodname'] = accum
                        accum = ''
                        state = MethodParseState.ParseArgs
                    pass
                case MethodParseState.ParseArgs:
                    if cr != ',' and cr != ')':
                        accum += cr
                    else:
                        accum = accum.strip()
                        if accum != '':
                            self.expr['methodparas'].append(accum)
                        accum = ''
                        state = MethodParseState.ParseArgs
                    if off == len(input) and cr == ')':
                        accum = accum.strip()
                        if accum != '':
                            self.expr['methodparas'].append(accum)
                        accum = ''
                        state = MethodParseState.End
                    pass
                case MethodParseState.End:
                    off -= 1
                    self.report2("method parse finished")
                    pass
            off += 1
        return self.expr