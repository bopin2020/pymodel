from core.expresstoken import *
from core.lexer import *

class MethodExpress: pass

class RootExpress(ConsoleLogable):
    def __init__(self):
        self.str = ""
        self.express = []
        self.builtinVar = {

        }
        self.ctxs = {}

        self.subexpress = ''
        self.tokens = []
        self.ctxtokens = []

    def register_context(self,name,ctx):
        self.ctxs[name] = ctx
        self.report(f'register {name} into context bag',1)

    def unregister_context(self,name):
        self.ctxs.pop(name)

    def format_objmodel(self):
        k = ""
        for x in self.ctxs.keys():
            k += f'\t {x}\n'
        return f'root\n {k}'

    def _eval(self,name,method,args):
        """Eval a short expression to invoke and return its value,such as
        obj.get_name()
        obj.name
        """
        try:
            if name not in self.ctxs.keys():
                raise ValueError(f'{name} object is invalid')

            if hasattr(self.ctxs[name],method):
                if self.tokens[0]['ismethod'] == 'true':
                    if args is None or len(args) == 0:
                        return getattr(self.ctxs[name],method)()
                    return getattr(self.ctxs[name],method)(*args)
                else:
                    return getattr(self.ctxs[name],method)
            else:
                raise ValueError(f'{name} object doesnt have {method}')
        except Exception as e:
            self.report(f'{str(e)}',2)
        return None
    
    def invoke(self,expression):
        try:
            # firstly, lexer tokenizer
            self.parse(expression)
            #
            # secondly,a single expression
            #
            if len(self.ctxtokens[0]) == 1:
                name,method,args = self.tokens[0]['objname'],self.tokens[0]['methodname'],self.tokens[0]['methodparas']
                return self._eval(name,method,args)
            else:
                #
                # eval expression
                #
                return self.operate()
        except Exception as e:
            self.report(f'{str(e)}',2)
        return None

    def _eval_left_right(self):
        name,objname,method,args = '','','',''
        tmp = ''
        index = 0
        for kv in self.ctxtokens[0]:
            match kv.type:
                case TokenType.Var:
                    pass
                case TokenType.LeftObjField:
                    name,objname,method,args = self.tokens[0]['name'],self.tokens[0]['objname'],self.tokens[0]['methodname'],self.tokens[0]['methodparas']
                    tmp = self._eval(objname,method,args)
                case TokenType.LeftObjMethod:
                    name,objname,method,args = self.tokens[0]['name'],self.tokens[0]['objname'],self.tokens[0]['methodname'],self.tokens[0]['methodparas']
                    tmp = self._eval(objname,method,args)
                case TokenType.Operation:
                    tmp = kv.str
                    if kv.str in ['==','-eq']:
                        tmp = Operate.EQ
                    if kv.str in ['!=','-ne']:
                        tmp = Operate.NE
                    if kv.str in ['>' , '-gt']:
                        tmp = Operate.GT
                    if kv.str in ['<' , '-lt']:
                        tmp = Operate.LT
                    if kv.str in ['>=' , '-ge']:
                        tmp = Operate.GE
                    if kv.str in ['<=' , '-le']:
                        tmp = Operate.LE    
                    if kv.str in ['in' , '-in']:
                        tmp = Operate.IN
                    if kv.str in ['ct' , '-ct']:
                        tmp = Operate.CONTAINS 
                case TokenType.RightObjField:
                    name,objname,method,args = self.tokens[1]['name'],self.tokens[1]['objname'],self.tokens[1]['methodname'],self.tokens[1]['methodparas']
                    tmp = self._eval(objname,method,args)
                case TokenType.RightObjMethod:
                    name,objname,method,args = self.tokens[1]['name'],self.tokens[1]['objname'],self.tokens[1]['methodname'],self.tokens[1]['methodparas']
                    tmp = self._eval(objname,method,args)
                case TokenType.Boundary:
                    pass
                case TokenType.BuiltInVar:
                    data = kv.str.strip('$')
                    if kv.str in builtinVar:
                        tmp = os.environ[data]
                case TokenType.BuiltInCustomVar:
                    pass
                case TokenType.Const:
                    self.report(kv.str)
                    if index > 0:
                        tmp = self.tokens[1]['name']
                        if '"' not in tmp:
                            tmp = int(tmp)
                    else:
                        tmp = self.tokens[0]['name']
            index += 1
            yield tmp

    def operate(self):
        """Make a determination between obj1 and obj2 which forms 
            1. obj eval expression(field and method return value)  
                                    =>  getpid() == getsessionid()
            2. object compare       => obj1 == obj2
            3. const compare        => 1 == 1    'bopin' == 'bopin'
        compare type in primitiveType
        """
        tmp = list(self._eval_left_right())
        match tmp[1]:
            case Operate.EQ:
                return tmp[0] == tmp[2]
            case Operate.NE:
                return tmp[0] != tmp[2]
            case Operate.GT:
                return tmp[0] > tmp[2]
            case Operate.LT:
                return tmp[0] < tmp[2]
            case Operate.GE:
                return tmp[0] >= tmp[2]
            case Operate.LE:
                return tmp[0] <= tmp[2]
            case Operate.IN:
                return tmp[0] in tmp[2]
            case Operate.CONTAINS:
                return tmp[2] in tmp[0]

    def eval(self,expression):
        pass

    def register_builtin_vars(self,var,value):
        """Append the built-in variables, for examples
        $faketrue ==>  1 == 1
        $enablefilter ==>  obj.disablefilter != $true
        $enablefilter ==>  obj->disablefilter != $true
        """
        builtinVar.append(var)
        self.builtinVar[var] = value

    def parse(self,input):
        self.tokens.clear()
        self.ctxtokens.clear()
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
                    self.report2("parse finished",1)
                    pass
                case ParseState.Error:
                    pass
                case ParseState.SubState:
                    ce = ChildExpress()
                    ce.parse(self.subexpress)
                    self.tokens.append(ce.left)
                    self.tokens.append(ce.right)
                    self.ctxtokens.append(ce.tokens)
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
        """Review state machine operations
        """
        self.tokens.clear()
        self.substr :str = input
        off = 0
        state = TokenState.LeftInit # type: ignore
        accum = ''
        curleft = True
        self.left['isvar'] = ''
        self.right['isvar'] = ''
        while off <= len(input):
            cr = input[off] if off < len(input)-0 else ''
            nr = input[off + 1]  if off < len(input)-1 else ''
            nnr = input[off + 2]  if off < len(input)-2 else ''
            #
            # 1. parse const and var, built-in var
            #       1 == 1
            #       "" == ""
            #       var1 == var2
            #       $true == $true
            # 2. parse obj fields and methods
            #       $obj.names -ct $obj.name
            # 
            #
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
                    if (cr not in c1) and (tag not in c1 and tag not in c2) and (tag2 not in c1 and tag2 not in c2) and off < len(input):
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
                                self.report(json.dumps(self.left,indent=4),4)
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
                        off += 2
                        continue
                    if tag2 in c2:
                        self.operation = tag2
                        self.tokens.append(Token(tag2,TokenType.Operation))
                        state = TokenState.RightInit
                        off += 2
                        continue
                    if cr == '>' or cr == '<':
                        self.operation = cr
                        self.tokens.append(Token(cr,TokenType.Operation))
                        state = TokenState.RightInit    
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
        """
        """
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