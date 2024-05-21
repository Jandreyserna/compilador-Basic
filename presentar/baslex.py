from rich import print
import sys
import sly
import re



class Lexer(sly.Lexer):
    reflags = re.IGNORECASE

    tokens = {
        # keywords
        LET, READ, DATA, PRINT, GOTO, IF,
        THEN, FOR, NEXT, TO, STEP, END,
        STOP, DEF, GOSUB, DIM, REM, RETURN,
        

        # operadores de relacion
        LT, LE, GT, GE, NE,

        #funciones adicionales
        INPUT, SIN, COS, TAN, ATN, EXP, ABS, LOG, SQR, RND, INT, TAB, TIME,
        # identificador
        ID, FN,

        # constantes
        INTEGER, FLOAT, STRING,

        #signo de concatenacion
        CONCAT,

    }
    literals = '+-*/^()=:,;'

    # ignorar
    ignore = ' \t'

    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')

    # expresiones regulares
    @_(r'REM.*\n')
    def REM(self, t):
        self.lineno += 1
        return t
    
    # Función para capturar la entrada del usuario
    @_(r'INPUT\s+"([^"]+)"')
    def INPUT(self, t):
        t.value = t.value.split('"')[1]  # Obtener el valor entre comillas
        return t
    
    INPUT = r'INPUT'
    SIN = r'SIN'
    COS = r'COS'
    TAN = r'TAN'
    ATN = r'ATN'
    EXP = r'EXP'
    ABS = r'ABS'
    LOG = r'LOG'
    SQR = r'SQR'
    RND = r'RND'
    INT = r'INT'
    TAB = r'TAB'
    TIME = r'TIME'

    LET    = r'LET' 
    READ   = r'READ'
    DATA   = r'DATA'
    PRINT  = r'PRINT'
    GOTO   = r'GO ?TO'
    IF     = r'IF'
    THEN   = r'THEN'
    FOR    = r'FOR'
    NEXT   = r'NEXT'
    TO     = r'TO'
    STEP   = r'STEP'
    END    = r'END'
    STOP   = r'STOP'
    DEF    = r'DEF'
    GOSUB  = r'GOSUB'
    DIM    = r'DIM'
    RETURN = r'RETURN'

    ID = r'[A-Z]([0-9]|[$])?'
    FN = r'FN[A-Z]'

    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'<>'
    INTEGER = r'\d+'
    FLOAT   = r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)'
    STRING  = r'"[^"]*"?'

    CONCAT = r'\+'


    def error(self, t):
        print(f"Línea {t.lineno}: [red]caracter ilegal '{t.value[0]}'[/red]")
        self.index += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python baslex.py source")
        exit(1)

    #test(open(sys.argv[1]).read())
    data = open(sys.argv[1]).read()

    lex = Lexer()
    for tok in lex.tokenize(data):
        print(tok)