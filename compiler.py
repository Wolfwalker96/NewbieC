import ply.yacc as yacc

from lex import tokens
import AST
from AST import addToClass

nbIndent=0
def getIndent():
    return "".join("\t" for i in range(nbIndent))

def compile(self):
    code = ""
    for c in self.children:
        code += c.compile()
    return code


@addToClass(AST.ProgramNode)
def compile(self):
    code = ""
    for c in self.children:
        code += c.compile()
    return code


@addToClass(AST.TokenNode)
def compile(self):
    code = ""
    code+="%s" % self.tok
    return code


@addToClass(AST.PrintNode)
def compile(self):
    code=""
    code+=getIndent()
    code+="cout <<  %s;\n" % self.children[0].tok
    return code


@addToClass(AST.AssignNode)
def compile(self):
    code=""
    code+=getIndent()
    code+="double %s" % self.children[0].tok
    code+=" = %s" % self.children[1].compile()
    code+=";\n"
    return code


@addToClass(AST.OpNode)
def compile(self):
    code=""
    code+=self.children[0].compile()
    code+=" %s " % self.op
    code+=self.children[1].compile()
    return code

@addToClass(AST.WhileNode)
def compile(self):
    code="while(cond)\n"
    code+="{"
    nbIndent+=1
    code+=getIndent()
    code+=self.children[0].compile()
    nbIndent-=1
    code+="}\n"
    return code


@addToClass(AST.IfNode)
def compile(self):
    code=""
    code+="if("
    code+=self.children[0].compile()
    code+=")\n"
    code+="{"
    nbIndent+=1
    code+=getIndent()
    code+=self.children[1].compile()
    nbIndent-=1
    code+="}\n"

    return code

@addToClass(AST.CondNode)
def compile(self):
    code=""
    code+=self.children[0].compile()
    code+=" "
    code+=self.op
    code+=" "
    code+=self.children[1].compile()

    return code


if __name__ == "__main__" :
    from parserNewbieC import parse
    import sys , os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+ '.c'
    outfile = open(name,'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote o u t p u t t o " , name)
