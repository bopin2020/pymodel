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
    ("ct","-ct"),
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

class Operate(IntEnum):
    EQ = 0,
    NE = 1,
    GT = 2,
    LT = 3,
    GE = 4,
    LE = 5,
    IN = 6,
    CONTAINS = 7

class MethodParseState(IntEnum):
    Init = 0,
    ParseArgs = 1,
    End = 2