import ply.yacc as yacc
import drawme_lex 
import sys

tokens = drawme_lex.tokens

def p_prog(p):
	'''prog : PR p2 p3 MAIN '''

def p_p2(p):
	'''p2 : globals 
| empty'''

def p_p3(p):
	'''p3 : functions 
| empty'''

def p_globals(p):
	'''globals : GL vars'''

def p_functions(p): 
	'''functions : FUN ID fun2 DP  SC'''

def p_fun2(p):
        '''fun2 : LP fun3 RP'''

def p_fun3(p):
	'''fun3 : type ID fun4 '''

def p_fun4(p):
	'''fun4 : C type ID fun4  
| empty'''



def p_empty(p):
    '''empty : '''

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!", p.type

# Build the parser
parser = yacc.yacc()

if(len(sys.argv) > 1):
    if sys.argv[1] == "-f":
        f = open(sys.argv[2], "r")
        s = f.readlines()
    string = ""
    for line in s:
        string += line
    result = parser.parse(string)
else:
    print "):"
