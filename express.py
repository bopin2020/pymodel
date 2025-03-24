from header import *

primitiveType = [
    #
    #  symbol, alias
    #
    ("==","-eq"),
    (">","-gt"),
    (">=","-ge"),
    ("<","-lt"),
    ("<=","-le"),
    ("!=","-ne"),
]

boundary = [
    ("&&","and"),
    ("||","or"),
]

obj = [
    (".","->")
]

symbols = [
    '(',
    ')',
    '{',
    '}'
]

#
#  register  environments
#
builtinVar = ["$true","$false","$null"]

def register_envs():
    [builtinVar.append(f'${x}') for x in list(os.environ)]

class ParseState(IntEnum):
    Init = 0,
    Complete = 1,
    Error = 2,
    SubState = 3,
    Operation = 4

class TokenState(IntEnum):
    LeftInit = 0,
    RightInit = 1,
    LeftObjIdentify = 2,
    RightObjIdentify = 3,
    BuiltInType = 4,
    StateBoundary = 5,
    Method = 6,
    End = 7,
    Unknown = 0xff

class TokenType(IntEnum):
    Var = 0,
    LeftObjField = 1,
    LeftObjMethod = 2,
    Operation = 3,
    RightObjField = 4,
    RightObjMethod = 5,
    Boundary = 6,
    BuiltInVar = 7,
    BuiltInCustomVar = 8,
    Const = 9

class Token():
    def __init__(self,data,type : TokenType):
        self.str = data
        self.type = type

    def __repr__(self):
        return f'{self.type.name}  {self.str}'

class Express():
    def __init__(self):
        pass

class RootExpress(ConsoleLogable):
    def __init__(self):
        self.str = ""
        self.express = []
        self.builtinVar = {

        }
        self.ctxs = {}

        self.subexpress = ''
        self.tokens = []

    def register_context(self,name,ctx):
        self.ctxs[name] = ctx

    def unregister_context(self,name):
        self.ctxs.pop(name)

    def format_objmodel(self):
        k = ""
        for x in self.ctxs.keys():
            k += f'\t {x}\n'
        return f'root\n {k}'
        
    def invoke(self,name,method,args,expression = "",ismethod = True):
        if hasattr(self.ctxs[name],method):
            if ismethod:
                if args is None:
                    return getattr(self.ctxs[name],method)()
                return getattr(self.ctxs[name],method)(*args)
            else:
                return getattr(self.ctxs[name],method)

    def register_builtin_vars(self,var,value):
        """Append the built-in variables, for examples
        $faketrue ==>  1 == 1
        $enablefilter ==>  obj.disablefilter != $true
        $enablefilter ==>  obj->disablefilter != $true
        """
        builtinVar.append(var)
        self.builtinVar[var] = value

    def parse(self,input):
        self.str = input
        off = 0
        state = ParseState.Init
        accum = ''
        while(off <= len(self.str)):
            cr = input[off] if off < len(input)-0 else ''
            nr = input[off + 1]  if off < len(input)-1 else ''
            nnr = input[off + 2]  if off < len(input)-2 else ''
            match state:
                case ParseState.Init:
                    tag = cr+nr
                    tag2 = cr+nr+nnr
                    c1 = list(map(lambda x: x[0],boundary))
                    c2 = list(map(lambda x: x[1],boundary))
                    if (tag not in c1 and tag not in c2) and (tag2 not in c1 and tag2 not in c2) and off < len(input):
                        accum += cr
                    else:
                        accum = accum.strip()
                        self.report(accum,0)
                        self.subexpress = accum
                        accum = ''
                        state = ParseState.SubState
                        if off == len(input):
                            off -= 1
                    pass
                case ParseState.Complete:
                    self.report("parse finished",1)
                    pass
                case ParseState.Error:
                    pass
                case ParseState.SubState:
                    ce = ChildExpress()
                    ce.parse(self.subexpress)
                    self.subexpress = ''
                    accum = ''
                    self.report(ce.tokens,2)
                    if off == len(input):
                        state = ParseState.Complete
                        off -= 1
                    else:
                        state = ParseState.Init
                case ParseState.Operation:
                    pass
            off += 1

class MethodExpress: pass

class ChildExpress(ConsoleLogable):
    def __init__(self):
        self.substr = ""
        self.left = {
            "name": "",
            "isobj": "",
            "isvar": "",
            "objname": "",
            "field": "",
            "ismethod": "",
            "methodname": "",
            "pref":"",
            "methodparas": [

            ]
        }
        self.operation = None
        self.right = {
            "name": "",
            "isobj": "",
            "isvar": "",
            "objname": "",
            "field": "",
            "ismethod": "",
            "methodname": "",
            "pref":"",
            "methodparas": [

            ]
        }

        self.tokens = []

    def is_method(self):
        print("reflec succ")
        pass

    def parse(self,input : str):
        self.tokens.clear()
        self.substr :str = input
        off = 0
        state = TokenState.LeftInit
        accum = ''
        curleft = True
        self.left['isvar'] = ''
        self.right['isvar'] = ''
        while off <= len(input):
            cr = input[off] if off < len(input)-0 else ''
            nr = input[off + 1]  if off < len(input)-1 else ''
            nnr = input[off + 2]  if off < len(input)-2 else ''
            match state:
                case TokenState.LeftInit:
                    if cr != '.' and (cr != '-' and nr != '>'):
                        accum += cr
                    else:
                        accum = accum.strip()
                        state = TokenState.LeftObjIdentify
                        self.left['name'] = accum
                        self.left['isobj'] = 'true'
                        self.left['objname'] = accum
                        self.left['pref'] = 'struct'
                        accum = ''
                    if cr == '-' and nr == '>':
                        self.left['pref'] = 'pointer'
                        off += 1
                    if cr == '$':
                        state = TokenState.BuiltInType
                case TokenState.RightInit:
                    if cr != '.' and (cr != '-' and nr != '>'):
                        accum += cr
                    else:
                        accum = accum.strip()
                        state = TokenState.RightObjIdentify
                        self.right['name'] = accum
                        self.right['isobj'] = 'true'
                        self.right['objname'] = accum
                        self.right['pref'] = 'struct'
                        accum = ''
                    
                    if off < len(input):
                        pass
                    else:
                        accum = accum.strip()
                        state = TokenState.End
                        # state = TokenState.RightObjIdentify
                        self.right['name'] = accum
                        self.right['isobj'] = 'false'
                        accum = ''      
                        off -= 1       

                    if cr == '-' and nr == '>':
                        self.right['pref'] = 'pointer'
                        off += 1
                    if cr == '$':
                        state = TokenState.BuiltInType
                case TokenState.LeftObjIdentify:
                    tag = cr+nr
                    tag2 = cr+nr+nnr
                    #print(f'{tag}  {tag2}')
                    c1 = list(map(lambda x: x[0],primitiveType))
                    c2 = list(map(lambda x: x[1],primitiveType))
                    if (tag not in c1 and tag not in c2) and (tag2 not in c1 and tag2 not in c2):
                        accum += cr
                    else:
                        accum = accum.strip()
                        if self.left['isvar'] != 'true':
                            if '(' in accum and ')' in accum:
                                self.left['ismethod'] = 'true'
                                self.left['methodname'] = accum
                                data = f'{self.left['objname']}{'->' if self.left['pref'] == 'pointer' else "."}{self.left['methodname']}'
                                self.report(data)
                                #
                                # parse  method args
                                #
                                result = MethodExpress().parse(self.left['methodname'])
                                self.left['methodname'] = result['methodname']
                                self.left['methodparas'] = result['methodparas']
                                print(json.dumps(self.left,indent=4))
                                self.tokens.append(Token(data,TokenType.LeftObjMethod))
                            else:
                                self.left['ismethod'] = 'false'
                                self.left['field'] = accum
                                data = f'{self.left['objname']}{'->' if self.left['pref'] == 'pointer' else "."}{self.left['field']}'
                                self.report(f'field=> {data}')
                                self.tokens.append(Token(data,TokenType.LeftObjField))
                        accum = ''
                    if tag in c1:
                        self.operation = tag
                        self.tokens.append(Token(tag,TokenType.Operation))
                        state = TokenState.RightInit    
                        off += 1   
                    if tag2 in c2:
                        self.operation = tag2
                        self.tokens.append(Token(tag2,TokenType.Operation))
                        state = TokenState.RightInit
                        off += 2
                case TokenState.RightObjIdentify:
                    if off < len(input):
                        accum += cr
                    else:
                        accum = accum.strip()
                        if self.right['isvar'] != 'true':
                            if '(' in accum and ')' in accum:
                                self.right['ismethod'] = 'true'
                                self.right['methodname'] = accum
                                data = f'{self.right['objname']}{'->' if self.right['pref'] == 'pointer' else "."}{self.right['methodname']}'
                                self.report(data)
                                result = MethodExpress().parse(self.right['methodname'])
                                self.right['methodname'] = result['methodname']
                                self.right['methodparas'] = result['methodparas']
                                print(json.dumps(self.right,indent=4))
                                self.tokens.append(Token(data,TokenType.RightObjMethod))
                            else:
                                self.right['ismethod'] = 'false'
                                self.right['field'] = accum
                                data = f'{self.right['objname']}{'->' if self.right['pref'] == 'pointer' else "."}{self.right['field']}'
                                self.report(f'field=> {data}')
                                self.tokens.append(Token(data,TokenType.RightObjField))
                        accum = ''                                        
                case TokenState.BuiltInType:
                    tag = cr+nr
                    tag2 = cr+nr+nnr
                    self.report(f'{tag}  {tag2}')
                    c1 = list(map(lambda x: x[0],primitiveType))
                    c2 = list(map(lambda x: x[1],primitiveType))
                    if (tag not in c1 and tag not in c2) and (tag2 not in c1 and tag2 not in c2):
                        accum += cr
                    else:
                        pass
                    accum = accum.strip()
                    if accum in builtinVar:
                        self.tokens.append(Token(accum,TokenType.BuiltInVar))
                        if curleft:
                            state = TokenState.LeftObjIdentify
                            self.left['isvar'] = 'true'
                            curleft = False
                        else:
                            state = TokenState.RightObjIdentify
                            self.right['isvar'] = 'true'
                            curleft = True
                        accum = ''
                case TokenState.End:
                    self.right['isobj'] = 'false'
                    self.right['pref'] = 'struct'
                    data = ''
                    if self.right['isobj'] == 'true':
                        data = f'{self.right['objname']}{'->' if self.right['pref'] == 'pointer' else "."}{self.right['methodname']}'
                    else:
                        data = f'{self.right['name']}'
                    self.report(data)
                    self.tokens.append(Token(data,TokenType.Const))              
                    break
            off += 1

    def invoke(self):
        pass

    def __repr__(self):
        if self.left['ismethod'] == 'true':
            pass
        else:
            pass

        if self.left['isobj'] == 'true':
            pass
        else:
            pass
        return f''


class MethodParseState(IntEnum):
    Init = 0,
    ParseArgs = 1,
    End = 2

class MethodExpress(ConsoleLogable):
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
                        self.expr['methodparas'].append(accum)
                        accum = ''
                        state = MethodParseState.ParseArgs
                    if off == len(input) and cr == ')':
                        accum = accum.strip()
                        self.expr['methodparas'].append(accum)
                        accum = ''
                        state = MethodParseState.End
                    pass
                case MethodParseState.End:
                    off -= 1
                    self.report("method parse finished")
                    pass
            off += 1
        return self.expr