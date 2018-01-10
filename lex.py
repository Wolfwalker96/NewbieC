import ply.lex as lex

tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'MULT',
   'DIV',
   'MOD',
   'LTH',
   'GTH',
   'EQU',
   'COND'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_LTH = r'<'
t_GTH = r'>'
t_EQU = r'='
t_COND = r'\?'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
