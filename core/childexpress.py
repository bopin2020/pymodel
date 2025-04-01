from core.expresstoken import *
from core.lexer import *
from core.methodexpress import *

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

    def is_const_expression(self, input : str):
        if input.startswith('\'') or input.startswith('"'):
            # string const
            return True
        
        if '.' not in input and '->' not in input:
            return True
        
        return False

    def parse(self,input : str):
        """Review state machine operations
        """
        self.tokens.clear()
        self.substr :str = input
        off = 0
        state = TokenState.LeftInit # type: ignore
        if self.is_const_expression(self.substr):
            state = TokenState.LeftConst
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
                    if cr == '"':
                        off -= 1
                        state = TokenState.RightConst
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
                    if cr == '"':
                        state = TokenState.RightConst
                case TokenState.LeftConst:
                    tag = cr+nr
                    tag2 = cr+nr+nnr
                    c1 = list(map(lambda x: x[0],primitiveType))
                    c2 = list(map(lambda x: x[1],primitiveType))
                    #
                    # peek keywords
                    # todo 
                    # 
                    if (cr not in c1) and (tag not in c1 and tag not in c2) and (tag2 not in c1 and tag2 not in c2) and off < len(input):
                        accum += cr
                    else:
                        accum = accum.strip()
                        state = TokenState
                        self.left['name'] = accum
                        self.left['isobj'] = 'false'
                        self.tokens.append(Token(self.left['name'],TokenType.LeftConst))
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
                    
                case TokenState.RightConst:
                    if off < len(input):
                        accum += cr
                    else:
                        accum = accum.strip()
                        state = TokenState.End
                        self.right['name'] = accum
                        self.right['isobj'] = 'false'
                        accum = ''
                        off -= 1
                case TokenState.LeftObjIdentify:
                    tag = cr+nr
                    tag2 = cr+nr+nnr
                    c1 = list(map(lambda x: x[0],primitiveType))
                    c2 = list(map(lambda x: x[1],primitiveType))
                    #
                    # peek keywords
                    # todo 
                    # 
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
                    # 
                    # 
                    #
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
                    self.tokens.append(Token(data,TokenType.RightConst))              
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