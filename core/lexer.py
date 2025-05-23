from core.header import *

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
    ("in","-in"),
    ("not in","-not in"),
    ("contains","-contains"),
    ("not contains","-not contains"),
]

boundary = [
    ("&&"," and "),
    ("||"," or "),
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

def unregister_envs():
    [builtinVar.append(f'${x}') for x in list(os.environ)]

def register_envs():
    [builtinVar.append(f'${x}') for x in list(os.environ)]

def reload_envs():
    unregister_envs()
    register_envs()

class ParseState(IntEnum):
    Init = 0,
    Complete = 1,
    Error = 2,
    SubState = 3,
    Operation = 4,
    EnterParenthesis = 5,       # (
    ExitParenthesis = 6,       # )

class TokenState(IntEnum):
    LeftInit = 0,
    RightInit = 1,
    LeftObjIdentify = 2,
    RightObjIdentify = 3,
    BuiltInType = 4,
    StateBoundary = 5,
    Method = 6,
    End = 7,
    LeftConst = 8,
    RightConst = 9,
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
    LeftConst = 9,
    RightConst = 10

class Operate(IntEnum):
    EQ = 0,
    NE = 1,
    GT = 2,
    LT = 3,
    GE = 4,
    LE = 5,
    IN = 6,
    NOTIN = 7,
    CONTAINS = 8,
    NOTCONTAINS = 9,

class MethodParseState(IntEnum):
    Init = 0,
    ParseArgs = 1,
    End = 2