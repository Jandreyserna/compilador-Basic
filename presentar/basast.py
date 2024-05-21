from dataclasses import dataclass
from multimethod import multimeta
from typing      import List, Union



# ---------------------------------------------------------------------
# Definicion Estructura del AST
# ---------------------------------------------------------------------
class Visitor(metaclass=multimeta):
    pass


@dataclass
class Node:
    pass

@dataclass
class Statement(Node):
    pass


@dataclass
class Expression(Node):
    pass

# --- Statement
@dataclass
class Program(Statement):
    cmds : List[Statement]

@dataclass
class InputStmt(Statement):
    vars: List[Expression]

@dataclass
class Command(Statement):
    lineno : int 
    command: Statement

@dataclass
class Let(Statement):
    var : Expression
    expr: Expression

@dataclass
class Read(Statement):
    varlist: List[Expression]

@dataclass
class Data(Statement):
    numlist: List[Expression]

@dataclass
class Input(Statement):
    varlist: List[Expression]

@dataclass
class Print(Statement):
    plist: Expression
    optend: str = None

@dataclass
class Goto(Statement):
    lineno: Expression

@dataclass
class IfStmt(Statement):
    relexpr: Expression
    lineno: Expression

@dataclass
class Remark(Statement):
    text : str 

@dataclass
class ForStmt(Statement):
    ident : Expression
    low   : Expression
    top   : Expression
    step  : Expression = None

@dataclass
class Next(Statement):
    ident : Expression

@dataclass
class End(Statement):
    pass

@dataclass
class Stop(Statement):
    pass

@dataclass
class Function(Statement):
    func : str
    param: Expression
    expr : Expression

@dataclass
class Gosub(Statement):
    lineno : Expression

@dataclass
class Return(Statement):
    pass

@dataclass
class Dim(Statement):
    dlist : Expression

# --- Expression

""" @dataclass
class Bltin(Expression):
    name : str
    expr : Expression """

@dataclass
class Bltin(Expression):
    name: str
    args: List[Expression] = None  # Lista para almacenar argumentos (opcional)

    def __init__(self, name: str, args: List[Expression] = None):
        self.name = name
        self.args = args

@dataclass
class Variable(Expression):
    name : str 

@dataclass
class Unary(Expression):
    op   : str
    expr : Expression

@dataclass
class Binary(Expression):
    op   : str
    left : Expression
    right: Expression

@dataclass
class Logical(Binary):
    pass

@dataclass
class Literal(Expression):
    pass

@dataclass
class Number(Literal):
    value : int | float

@dataclass
class String(Literal):
    value : str
    expr : Expression = None

@dataclass
class Input(Statement):
    label  : str
    varlist: List[Expression]

@dataclass
class Bltin(Expression):
    name : str
    expr : Expression

@dataclass
class Program(Statement):
    cmds: List[Union[Statement, InputStmt]]

@dataclass
class Group(Expression):
    expr: Expression
    def accept (self, visitor):
        return visitor.visit_Group(self) 

@dataclass
class PrintStmt(Expression):
    expr: Expression

