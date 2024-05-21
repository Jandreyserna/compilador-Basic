from rich import print
import sly

from baslex import Lexer
from basast import *
from basrender import DotRenderer

class SyntaxError(Exception):
    pass

class Parser(sly.Parser):
    debugfile = 'parse.txt'
    tokens = Lexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', '^'),
        ('right', UMINUS),
    )

    @_("{ statement }")
    def program(self, p):
        return Program(p.statement)

    @_("INTEGER command")
    def statement(self, p):
        return Command(p.INTEGER, p.command)

    @_("LET variable '=' expr")
    def command(self, p):
        return Let(p.variable, p.expr)

    @_("READ varlist")
    def command(self, p):
        return Read(p.varlist)

    """ @_("DATA numlist")
    def command(self, p):
        pass """
    
    @_("DATA numlist")
    def command(self, p):
        return DataStmt(p.numlist)

    """ @_("PRINT plist optend")
    def command(self, p):
        pass """
    
    @_("PRINT plist optend")
    def command(self, p):
        return PrintStmt((p.plist, p.optend))

    """ @_("GOTO INTEGER")
    def command(self, p):
        pass """
    
    @_("GOTO INTEGER")
    def command(self, p):
        return GotoStmt(p.INTEGER)

    """ @_("IF relexpr THEN INTEGER")
    def command(self, p):
        pass """
    
    @_("IF relexpr THEN INTEGER")
    def command(self, p):
        return IfStmt(p.relexpr, p.INTEGER)

    @_("FOR ID '=' expr TO expr optstep")
    def command(self, p):
        return ForStmt(Variable(p.ID), p.expr0, p.expr1, p.optstep)

    @_("NEXT ID")
    def command(self, p):
        return Next(Variable(p.ID))

    @_("END")
    def command(self, p):
        return End()

    @_("REM")
    def command(self, p):
        return Remark(p.REM[4:])

    """ @_("STOP")
    def command(self, p):
        pass """
    
    @_("STOP")
    def command(self, p):
        return StopStmt()


    """ @_("DEF FN '(' ID ')' '=' expr")
    def command(self, p):
        pass """
    
    @_("DEF FN '(' ID ')' '=' expr")
    def command(self, p):
        return DefFnStmt(p.ID, p.expr)


    """ @_("GOSUB INTEGER")
    def command(self, p):
        pass """
    
    @_("GOSUB INTEGER")
    def command(self, p):
        return GosubStmt(p.INTEGER)

    """ @_("RETURN")
    def command(self, p):
        pass """
    
    @_("RETURN")
    def command(self, p):
        return ReturnStmt()

    """ @_("DIM dimlist")
    def command(self, p):
        pass """
    
    @_("DIM dimlist")
    def command(self, p):
        return DimStmt(p.dimlist)

    @_("expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr",
       "expr '^' expr")
    def expr(self, p):
        return Binary(p[1], p.expr0, p.expr1)

    @_("variable")
    def expr(self, p):
        return p.variable

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        return Unary(p[0], p.expr)

    @_("expr LT expr",
       "expr LE expr",
       "expr GT expr",
       "expr GE expr",
       "expr '=' expr",
       "expr NE expr")
    def relexpr(self, p):
        return Logical(p[1], p.expr0, p.expr1)

    @_("ID")
    def variable(self, p):
        return Variable(p.ID)

    @_("ID '(' INTEGER ')'")
    def variable(self, p):
        pass

    @_("ID '(' INTEGER ',' INTEGER ')'")
    def variable(self, p):
        pass

    @_("','", "';'", "empty")
    def optend(self, p):
        pass

    @_("STEP expr")
    def optstep(self, p):
        return p.expr

    @_("empty")
    def optstep(self, p):
        pass

    @_("dimitem { dimitem }")
    def dimlist(self, p):
        return [p.dimitem0] + p.dimitem1

    @_("ID '(' INTEGER ')'")
    def dimitem(self, p):
        pass

    @_("ID '(' INTEGER ',' INTEGER ')'")
    def dimitem(self, p):
        pass

    @_("variable { ',' variable }")
    def varlist(self, p):
        return [p.variable0] + p.variable1

    @_("number { ',' number }")
    def numlist(self, p):
        return [p.number0] + p.number1

    @_("INTEGER")
    def number(self, p):
        return Number(p[0])

    @_("'-' INTEGER %prec UMINUS")
    def number(self, p):
        pass

    # Regla pitem para manejar los INTEGER como pitems independientes
    @_("INTEGER")
    def pitem(self, p):
        return Number(p.INTEGER)

    # Regla adicional para manejar la repetición de elementos en plist
    @_("pitem",
       "plist ',' pitem")  
    def plist(self, p):
        if len(p) == 1:
            return [p.pitem]
        else:
            return p.plist + [p.pitem]

    @_("STRING")
    def pitem(self, p):
        return String(p.STRING[1:-1])

    @_("STRING expr")
    def pitem(self, p):
        pass

    @_("expr")
    def pitem(self, p):
        pass

    @_("")
    def empty(self, p):
        pass

    @_(r"INPUT [ STRING ',' ] varlist")
    def command(self, p):
        return InputStmt((p.STRING, p.varlist))

    @_("SIN '(' expr ')'")
    def expr(self, p):
        return Function('SIN', p.expr)
    
    def error(self, p):
        # Imprimir un mensaje más detallado sobre el error de sintaxis
        print("Error de Sintaxis:")
        print("Tipo de Error:", p.type)  # Tipo de error
        print("Token Actual:", p.value)  # Token actual que causó el error
        print("Línea:", p.lineno)        # Número de línea donde ocurrió el error
        print("Posición:", p.index)       # Posición dentro de la línea donde ocurrió el error

def test(txt):
    l = Lexer()
    p = Parser()

    try:
        top = p.parse(l.tokenize(txt))
        print(top)
        dot = DotRenderer()
        #top.accept(dot)
        print(dot.dot)
    except SyntaxError as e:
        print(e)
        # Obtener la información adicional del token donde ocurrió el error
        token = e.token
        if token:
            print("Token donde ocurrió el error:", token.type)
            print("Línea:", token.lineno)
            print("Posición:", token.index)
        else:
            print("No se pudo obtener información adicional sobre el error.")

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("usage: python basparse.py source")
        exit(1)

    test(open(sys.argv[1]).read())
