import ply.yacc as yacc

from lex import tokens
import AST
from AST import addToClass

nbIndent={}
nbI=0
forVarDic = {}
forStepDic = {}
currentFor = "i0"
functionNames = []

def getIndent():
    return "".join("\t" for i in range(nbIndent[functionNames[-1]]))

def compile(self):
    code = ""
    code += "#include <stdio.h>\n"
    code += "#include <stdlib.h>\n\n"
    for c in self.children:
        code += c.compile()
    return code

@addToClass(AST.MainNode)
def compile(self):
    global functionNames
    global nbIndent
    functionNames.append("main")
    nbIndent[functionNames[-1]]=0
    code = "int main()\n{\n"
    nbIndent[functionNames[-1]]+=1
    for c in self.children:
        code += c.compile()
    nbIndent[functionNames[-1]]-=1
    code +="}\n"
    functionNames.pop()
    return code

@addToClass(AST.FunctionNode)
def compile(self):
    global functionNames
    functionNames.append(self.tok)
    nbIndent[functionNames[-1]]=1
    code = f"double {self.tok}("

    if len(self.children) == 2:
        try:
            code+=self.children[1].compile()
            code+=")\n{\n"
        except:
            pass
        try:
            code+=self.children[0].compile()
            code+="\n"
        except:
            pass
    else:
        code+=")\n{\n"
        code+=self.children[0].compile()
        code+="\n"

    code+="}\n\n"

    nbIndent[functionNames[-1]]-=1
    functionNames.pop()
    return code

@addToClass(AST.ParameterNode)
def compile(self):
    code = ""
    code += "double "
    code += self.children[0].compile()
    try:
        code += ", %s" % self.children[1].compile()
    except:
        pass
    return code

@addToClass(AST.ReturnNode)
def compile(self):
    code = ""
    code+=getIndent()
    code += "return "
    code += self.children[0].compile()
    code += ";"
    return code


@addToClass(AST.CallNode)
def compile(self):
    code = f"{self.tok}("
    code+=self.children[0].compile()
    code+=")\n"
    return code

@addToClass(AST.ArgumentNode)
def compile(self):
    code = ""
    try:
        code += self.children[0].compile()
    except:
        pass
    try:
        code += ", %s" % self.children[1].compile()
    except:
        pass
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
    if '"' in  self.children[0].compile():
        code+="printf(\"%%s\",%s);\n" % self.children[0].compile()
    else:
        code+="printf(\"%%d\",%s);\n" % self.children[0].compile()
    return code


@addToClass(AST.AskNode)
def compile(self):
    code=""
    if len(self.children) == 1 :
        code+=getIndent()
        code+="double %s;\n" % self.children[0].compile()
        code+=getIndent()
        code+="scanf(\"%%d\",&%s);\n" % self.children[0].compile()
    else:
        code+=self.children[0].compile()
        code+=getIndent()
        code+="double %s;\n" % self.children[1].compile()
        code+=getIndent()
        code+="scanf(\"%%d\",&%s);\n" % self.children[1].compile()
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
    nbIndent[functionNames[-1]]+=1
    code+=getIndent()
    code+=self.children[0].compile()
    nbIndent[functionNames[-1]]-=1
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
    nbIndent[functionNames[-1]]+=1
    try:
        code+=self.children[1].compile()
    except:
        pass
    nbIndent[functionNames[-1]]-=1
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
    global nbIndent
    global currentFor
    global nbI
    code=""

    nbI += 1
    currentFor = "i%s" % nbI

    code+=self.children[0].compile()
    code+=self.children[1].compile()

    nbIndent[functionNames[-1]]-=1
    code+=getIndent()
    code+="}\n"

    nbI -= 1
    currentFor = "i%s" % nbI
    return code


@addToClass(AST.RangeNode)
def compile(self):
    global nbIndent
    global forStackDic
    global forStepDic
    global currentFor

    code=""
    varName = ""
    step = ""

    if currentFor in forVarDic:
        varName = forVarDic[currentFor]
    else:
        varName = currentFor

    if currentFor in forStepDic:
        step = forStepDic[currentFor]
    else:
        step = "1"

    code+=getIndent()
    code+=f"int {varName};\n"
    code+=getIndent()
    code+="for(%s=" % varName
    code+=self.children[0].compile()
    code+=";%s<" % varName
    code+=self.children[1].compile()
    code+=";%s" % varName
    code+="+=%s)\n" % step
    code+=getIndent()
    code+="{\n"
    nbIndent[functionNames[-1]]+=1

    return code


@addToClass(AST.StepNode)
def compile(self):
    global forStepDic
    global currentFor

    code=""
    forStepDic[currentFor]=self.children[1].compile()
    code+=self.children[0].compile()
    return code


@addToClass(AST.InNode)
def compile(self):
    global forStackDic
    global currentFor

    code=""
    forVarDic[currentFor]=self.children[1].compile()
    code+=self.children[0].compile()
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
