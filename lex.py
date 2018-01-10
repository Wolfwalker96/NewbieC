import ply.lex as lex

reserved_words = (
    'else',
    'to',
    'in',
    'say',
    'is',
    'step',
    'return',
    'not',
    'and',
    'or',
    'between',
    'main',
    'ask'
)

tokens = (
    'NUMBER',
	'ADD_OP',
	'MUL_OP',
    'MOD',
    'LTH',
    'GTH',
    'EQU',
    'COND',
    'STRING'
) + tuple(map(lambda s:s.upper(),reserved_words))

t_MOD = r'%'
t_LTH = r'<'
t_GTH = r'>'
t_EQU = r'='
t_COND = r'\?'

literals = '()\t'

def t_ADD_OP(t):
	r'\+|-'
	return t

def t_MUL_OP(t):
	r'\*|/'
	return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'".*"'
    t.value = str(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' '


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
