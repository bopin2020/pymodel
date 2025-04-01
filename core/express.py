from core.expresstoken import *
from core.lexer import *
from core.childexpress import *

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
        self.ctxresults = []
        self.component_expression = []

    def reload_context(self,name,ctx):
        self.ctxs[name] = ctx
        #self.report(f're-register {name} into context bag',1)

    def register_context(self,name,ctx):
        self.ctxs[name] = ctx
        self.report(f'register {name} into context bag',1)

    def unregister_context(self,name):
        self.ctxs.pop(name)
        self.report(f'unregister {name} from context bag',1)

    def unregister_contexts(self):
        tmp = list(self.ctxs.keys())
        for k in tmp:
            self.unregister_context(k)

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
                if self.tokens[0]['ismethod'] == 'true':
                    name,method,args = self.tokens[0]['objname'],self.tokens[0]['methodname'],self.tokens[0]['methodparas']
                    result = self._eval(name,method,args)
                    self.report3(f'eval the single expression: {result}',2)
                else:
                    objname,field = self.tokens[0]['objname'],self.tokens[0]['field']
                    result = self._eval(objname,field,[])
                    self.report3(f'eval the single expression: {result}',2)
                return result
            else:
                #
                # eval expression
                #
                for token in self.ctxtokens:
                    self.ctxresults.append(self.operate(list(self._map_to_value(token))))
                return self.ctxresults
        except Exception as e:
            self.report(f'{str(e)}',2)
        return None

    def _map_to_value(self,ctxtoken):
        """Map the expression to get values and built-in var
        """
        name,objname,method,args = '','','',''
        tmp = ''
        index = 0
        for kv in ctxtoken:
            match kv.type:
                case TokenType.Var:
                    pass
                case TokenType.LeftObjField:
                    if self.tokens[0]['ismethod'] == 'true':
                        name,objname,method,args = self.tokens[0]['name'],self.tokens[0]['objname'],self.tokens[0]['methodname'],self.tokens[0]['methodparas']
                        tmp = self._eval(objname,method,args)
                    else:
                        objname,field = self.tokens[0]['objname'],self.tokens[0]['field']
                        tmp = self._eval(objname,field,[])
                        self.report3(f'eval the single expression: {tmp}',2)

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
                    if kv.str in ['not in' , '-not in']:
                        tmp = Operate.NOTIN
                    if kv.str in ['not contains' , '-not contains']:
                        tmp = Operate.NOTCONTAINS
                    if kv.str in ['contains' , '-contains']:
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
                case TokenType.LeftConst:
                    self.report(kv.str,2)
                    try:
                        #
                        # const parse
                        #
                        tmp : str = self.tokens[0]['name']
                        if '"' in self.tokens[0]['name']:                                              #
                            # single or double quotes
                            #
                            tmp = tmp.strip('"').strip('\'')


                        # try convert str to int
                        if not tmp.startswith('\'') and not tmp.startswith('\"'):
                            if tmp.startswith('0x'):
                                tmp = int(tmp,16)
                            else:
                                tmp = int(tmp)
                    except:
                        self.report3("const value type parse error")
                case TokenType.RightConst:
                    self.report(kv.str)
                    try:
                        #
                        # const parse
                        #
                        tmp : str = self.tokens[1]['name']
                        if '"' in self.tokens[1]['name']:                                              #
                            # single or double quotes
                            #
                            tmp = tmp.strip('"').strip('\'')


                        # try convert str to int
                        if not tmp.startswith('\'') and not tmp.startswith('\"'):
                            if tmp.startswith('0x'):
                                tmp = int(tmp,16)
                            else:
                                tmp = int(tmp)
                    except:
                        self.report3("const value type parse error")
            index += 1
            yield tmp

    def operate(self,tmp):
        """Make a determination between obj1 and obj2 which forms 
            1. obj eval expression(field and method return value)  
                                    =>  getpid() == getsessionid()
            2. object compare       => obj1 == obj2
            3. const compare        => 1 == 1    'bopin' == 'bopin'
        compare type in primitiveType
        """
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
        self.ctxresults.clear()
        self.tokens.clear()
        self.ctxtokens.clear()
        self.str = input
        off = 0
        state = ParseState.Init
        accum = ''
        componenttokens = []
        while(off <= len(self.str)):
            cr = input[off] if off < len(input)-0 else ''
            nr = input[off + 1]  if off < len(input)-1 else ''
            nnr = input[off + 2]  if off < len(input)-2 else ''
            match state:
                case ParseState.Init:
                    tag = cr+nr
                    tag2 = cr+nr+nnr
                    #
                    # todo   keyword check
                    #
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
                    self.report2(f'childexpress {ce.tokens}',2)
                    if off == len(input):
                        state = ParseState.Complete
                        off -= 1
                    else:
                        state = ParseState.Init
                case ParseState.Operation:
                    pass
                case ParseState.EnterParenthesis:
                    # parse  component expression
                    componenttokens.clear()
                    state = ParseState.Init
                    pass
                case ParseState.ExitParenthesis:
                    # parse component expression finish
                    pass
            off += 1