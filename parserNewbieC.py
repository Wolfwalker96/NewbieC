import ply.yacc as yacc
from lex import tokens
import AST

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right','UMINUS')
)

vars = {}

def p_programme_recursive(p):
    ''' programme : statement NEWLINE programme
            | structure NEWLINE programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_programme_statement(p):
    ''' programme : statement NEWLINE
            | structure NEWLINE'''
    p[0] = AST.ProgramNode(p[1])

def p_statement_say(p):
    ''' statement : SAY expression '''
    p[0] = AST.PrintNode(p[2])

def p_statement_say_string(p):
    ''' statement : SAY STRING '''
    p[0] = AST.PrintNode(AST.TokenNode(p[2]))

def p_statement_ask(p):
    '''statement : ASK IDENTIFIER '''
    p[0] = AST.AskNode(AST.TokenNode(p[2]))

def p_statement_ask_string(p):
    '''statement : ASK STRING IN IDENTIFIER'''
    p[0] = AST.AskNode([AST.PrintNode(AST.TokenNode(p[2])), AST.TokenNode(p[4])])

def p_structure_conditional(p):
    ''' structure : condstruct '''
    p[0] = p[1]

def p_structure_cond(p):
    ''' condstruct : condition '?' NEWLINE programme END'''
    p[0] = AST.IfNode([p[1], p[4]])

def p_structure_elseif(p):
    ''' condstruct : ELSE condition '?' NEWLINE programme END'''
    p[0] = AST.IfNode([p[2], p[5]])

def p_structure_else(p):
    ''' condstruct : ELSE '?' NEWLINE programme END'''
    p[0] = AST.IfNode([p[4]])


def p_structure_for(p):
    '''structure : for NEWLINE programme END'''
    p[0] = AST.ForNode([p[1], p[3]])


def p_range(p):
    ''' for : expression TO expression '''
    p[0] = AST.RangeNode([p[1], p[3]])


def p_in(p):
    ''' for : for IN IDENTIFIER '''
    p[0] = AST.InNode([p[1], AST.TokenNode(p[3])])


def p_step(p):
    ''' for : for STEP expression '''
    p[0] = AST.StepNode([p[1], p[3]])


def p_structure_function(p):
    ''' structure : IDENTIFIER NEWLINE programme END '''
    p[0] = AST.FunctionNode(p[1], [p[3]])

def p_structure_function_with_parameter(p):
    ''' structure : IDENTIFIER parameter NEWLINE programme END '''
    p[0] = AST.FunctionNode(p[1], [p[4], p[2]])

def p_function_parameter_rec(p):
    ''' parameter : IDENTIFIER ',' parameter '''
    p[0] = AST.ParameterNode([AST.TokenNode(p[1]), p[3]])

def p_function_parameter(p):
    '''parameter : IDENTIFIER '''
    p[0] = AST.ParameterNode(AST.TokenNode(p[1]))

def p_function_return(p):
    '''statement : RETURN expression '''
    p[0] = AST.ReturnNode(p[2])

def p_function_call(p):
    ''' expression : IDENTIFIER argument '''
    p[0] = AST.CallNode(p[1], [p[2]])

def p_function_call_parameter_rec(p):
    ''' argument : expression ',' argument '''
    p[0] = AST.ArgumentNode([AST.TokenNode(p[1]), p[3]])

def p_function_call_parameter(p):
    '''argument : expression '''
    p[0] = AST.ArgumentNode(AST.TokenNode(p[1]))

def p_condition(p):
    ''' condition : expression COND_OP expression '''
    p[0] = AST.CondNode(p[2], [p[1], p[3]])

def p_condition_recursive(p):
    ''' condition : condition AND condition
        | condition OR condition '''
    p[0] = AST.CondNode(p[2], [p[1], p[3]])

def p_statement(p):
    '''statement : expression
        | assignation '''
    p[0] = p[1]


def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])


def p_expression_op(p):
    '''expression : expression ADD_OP expression
        | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])


def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_assign(p):
    ''' assignation : IDENTIFIER IS expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_structure_main(p):
    ''' structure : MAIN NEWLINE programme END '''
    p[0] = AST.MainNode(p[3].children)


def p_error(p):
    if p is not None:
        print("Erreur de syntaxe à la ligne %s" % p.lineno)
        print(p)
    else:
        print("Unexpected end of input")


def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    if result:
        print(result)

        import os

        os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Pasing returned no result")
