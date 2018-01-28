import ply.yacc as yacc

from lex import tokens
import AST
from AST import addToClass

nbIndent=0
nbI=0;
def getIndent():
    return "".join("\t" for i in range(nbIndent))

def compile(self):
    code = ""
    for c in self.children:
        code += c.compile()
    return code

@addToClass(AST.MainNode)
def compile(self):
    code = "int main()\n{\n"
    global nbIndent
    nbIndent+=1
    for c in self.children:
        code += c.compile()
    nbIndent-=1
    code +="}\n"
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
    if '"' in  self.children[0].tok:
        code+="printf(\"%%s\",%s);\n" % self.children[0].tok
    else:
        code+="printf(\"%%d\",%s);\n" % self.children[0].tok
    return code


@addToClass(AST.AskNode)
def compile(self):
    code=""
    code+=getIndent()
    code+=getIndent()
    code+="double %s" % self.children[0].tok
    code+=getIndent()
    code+="scanf(\"%%d\",&%s);\n" % self.children[0].tok
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
    global nbIndent
    code+=getIndent()
    code="while("
    code+=self.children[0].compile()
    code+=")\n"
    code+=getIndent()
    code+="{"
    nbIndent+=1
    code+=getIndent()
    code+=self.children[0].compile()
    nbIndent-=1
    code+="}\n"
    return code


@addToClass(AST.IfNode)
def compile(self):
    global nbIndent
    code=""
    code+=getIndent()
    code+="if("
    code+=self.children[0].compile()
    code+=")\n"
    code+=getIndent()
    code+="{\n"
    nbIndent+=1
    code+=self.children[1].compile()
    nbIndent-=1
    code+=getIndent()
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

    code = code.replace("or","||")
    code = code.replace("and","&&")
    return code

@addToClass(AST.ForNode)
def compile(self):
    nbIndent
    i = "i%s" % nbI
    nbI += 1
    code+="int %s" % i
    code+="for(%s=" % i
    code+=self.children[0].compile()
    code+="; %s < " %s
    code+=self.children[1].tok
    code+=";%s++)\n" % i
    code+="{"
    nbIndent+=1
    code+=getIndent()
    code+=self.children[1].compile()
    nbIndent-=1
    code+="}\n"

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
