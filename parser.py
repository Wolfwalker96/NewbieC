import ply.yacc as yacc
from lex import tokens
import AST

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

vars = {}

def p_programme_recursive(p):
	''' programme : statement \t programme '''
	p[0] = AST.ProgramNode([p[1]]+p[3].children)


def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])


def p_statement(p):
    '''statement : expression
        | assignation'''
    p[0] = p[1]


def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER'''
    p[0] = AST.TokenNode(p[1])


def p_expression_op(p):
    '''expression : expression ADD_OP expression
        | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2],[p[1], p[3]])


def p_minus(p):
	''' expression : ADD_OP expression %prec UMINUS'''
	p[0] = AST.OpNode(p[1], [p[2]])


def p_expression_paren(p):
	'''expression : '(' expression ')' '''
	p[0] = p[2]


def p_assign(p):
	''' assignation : IDENTIFIER IS expression '''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])



def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.errok()


yacc.yacc(outputdir='generated')


if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    if result:
        print(result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Pasing returned no result")
