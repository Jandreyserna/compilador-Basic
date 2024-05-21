# basinter.py
'''
Analisis Semántico & Interprete para BASIC DARTMOUTH 64

En el analisis Semantico, debemos realizar:

1. Verificar que todos los IDENT esten definidos
   LET / FOR / READ / DIM / INPUT ...
2. Un programa en BASIC solo debe contener una instruccion END y 
   debe de estar en la ultima linea.
3. Revisar las Instrucciones FOR/NEXT
4. Revisar las instrucciones READ/DATA
5. Recolectar los valores de la Instrucción DATA en una list
'''
import math
import random

from typing import Dict, Union
from basast import *

class Interpreter(Visitor):
    def __init__(self, prog):
        self.prog = prog

        self.functions = {
            'SIN'  : lambda x: math.sin(x),
            'COS'  : lambda x: math.cos(x),
            'TAN'  : lambda x: math.tan(x),
            'ATN'  : lambda x: math.atan(x),
            'EXP'  : lambda x: math.exp(x),
            'ABS'  : lambda x: abs(x),
            'LOG'  : lambda x: math.log(x),
            'SQR'  : lambda x: math.sqrt(x),
            'INT'  : lambda x: int(x),
            'RND'  : lambda x: random.random(),
            'LEFT$': lambda x,n  : x[:n],
            'MID$' : lambda x,m,n: x[m:n],
            'RIGHT$': lambda x,n : x[-n:]

        }
    
    @classmethod
    def interp(cls, prog:Dict[int, Statement]):
        basic = cls(prog)
        basic.run()
    
    # Interprete

    # Analisis Semantico (chequeos)
    def collect_data(self):
        '''
        Organizar los datos en la instrucción DATA dentro de una list
        '''
        self.dc = 0

    def check_end(self):
        '''
        Un programa en BASIC solo debe contener una instrucción END
        y esta debe de estar en la ultima linea.
        '''
        pass

    def check_loops(self):
        '''
        Revisar las instrccuines FOR/NEXT
        '''
        pass

    def run(self):
        # Tabla de Simbol
        self.vars   = {}        # All variables
        self.lists  = {}        # list variables
        self.tables = {}        # Tables
        self.loops  = {}        # Currently active loops
        self.loopend = {}       # Mappinf saying where loop end
        self.gosub  = None      # Gosub return
        self.error  = False     # Indicates program error

        self.stat = list(self.prog) # Ordered list of all line numbers
        self.stat.sort()
        self.pc   = 0           # Current program counter

        # Preprocesamiento antes de ejecutar

        self.collect_data()
        self.check_end()
        self.check_loops()

    # Patron Visitor

    def visit(self, n: Let):
        pass

    def visit(self, n: Read):
        pass

    def visit(self, n: Data):
        pass

    def visit(self, n: Print):
        pass

    def visit(self, n: Input):
        pass

    def visit(self, n: Goto):
        pass

    def visit(self, n: IfStmt):
        pass

    def visit(self, n: ForStmt):
        pass

    def visit(self, n: Next):
        pass

    def visit(self, n: End):
        pass

    def visit(self, n: Remark):
        pass

    def visit(self, n: Stop):
        pass

    # Expression Nodes

    def visit(self, n: Group):
        pass

    def visit(self, n: Binary):
        pass

    def visit(self, n: Unary):
        pass

    def visit(self, n: Literal):
        pass

    def visit(self, n: Variable):
        pass    