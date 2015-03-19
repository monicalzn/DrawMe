import ply.yacc as yacc
import drawme_lex 
import sys
import re

from stack import Stack
from avail import avail

tokens = drawme_lex.tokens
ht = dict()
funPar = dict()
vType = None
proDict = dict()
scope = None
idFunc = None
avail = avail()
OStack = Stack()  #Operand Stack
TStack = Stack() #Type stack
OpStack = Stack() #Operator stack
quads = [] #Quadruples queue
funCheck = [] #Check function parameters
numQuad = 0

def p_prog(p):
	'''prog : PR p2 p3 MAIN vars block'''
	proDict["main"] = ht
	print numQuad
	print quads

def p_p2(p):
	'''p2 : globals 
| empty'''

def p_p3(p):
	'''p3 : functions p3
| empty'''

def p_globals(p):
	'''globals : GL vars'''
	vaDict = dict(ht)
	proDict["globals"] = vaDict
	ht.clear()

def p_functions(p): 
	'''functions : fun2 DP vars block'''	
	ht.clear()

def p_fun2(p):
        '''fun2 : FUN ID LP fun3 RP'''
	vaDict = dict(funPar)
	proDict[p[2]] = vaDict
	funPar.clear()
	

def p_fun3(p):
	'''fun3 : fun5 fun4
| empty'''
	

def p_fun4(p):
	'''fun4 : C fun5 fun4  
| empty'''

def p_fun5(p):
	'''fun5 : type ID '''
	ht[p[2]] = [vType, "var"]
	funPar[p[2]] = [vType, "var"]

def p_vars(p): 
	'''vars : V var2 var5
| empty'''

def p_var2(p):
        '''var2 : type var3 SC var2
| empty'''

def p_var3(p):
	'''var3 : ID var4 var33 '''
	if p[1] in ht:
		print "Existing var, ", p[1]
	else:
		ht[p[1]] = [vType, "var"]

def p_var33(p):
	'''var33 : C ID var4 var33 
| empty '''
	if(len(p) == 5):
		if p[2] in ht:
			print "Existing var, ", p[2]
		else:
			ht[p[2]] = [vType, "var"]

def p_var4(p):
        '''var4 : EQ exp 
| empty'''

def p_var5(p):
	'''var5 : list var5
| empty'''

def p_type(p):
	'''type : INT 
| FLOAT  '''
	global vType
	vType = p[1]

def p_val(p):
	'''val : VALI 
| VALF  '''

def p_position(p):
	'''position : PENP LP exp C exp RP SC'''
	spCuad = [307, OStack.pop(), OStack.pop(), -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_colors(p):
	'''colors : PENC LP exp C exp C exp RP SC 
| SETC LP exp C exp C exp RP SC 
| BACO LP exp C exp C exp RP SC '''
	if(p[1] == 'penColor'):
		spCuad = [301, OStack.pop(), OStack.pop(), OStack.pop()]
	elif(p[1] == 'setColor'):
		spCuad = [302, OStack.pop(), OStack.pop(), OStack.pop()]
	else:
		spCuad = [303, OStack.pop(), OStack.pop(), OStack.pop()]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1


def p_p_width(p):
	'''p_width : PENW LP exp RP SC '''
	spCuad = [304, OStack.pop(), OStack.pop(), -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_penwrite(p):
	'''penwrite : PENU SC 
| PEND SC'''
	if(p[1] == 'penUp'):
		spCuad = [308, -1, -1, -1]
	else:
		spCuad = [309, -1, -1, -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_move(p):
	'''move : F mueve2
| B mueve2'''

def p_mueve2(p):
	'''mueve2 : LP exp C A exp RP SC'''

def p_rect(p):
	'''rect : REC LP exp C exp p_fill RP SC'''
	spCuad = [201, OStack.pop(), OStack.pop(), -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_p_fill(p):
	'''p_fill : C FILL 
| empty'''
	if(len(p) == 3):
		spCuad = [209, -1, -1, 1]
	else:
		spCuad = [209, -1, -1, -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_tria(p):
	'''tria : TRI LP exp C exp C exp p_fill RP SC'''
	spCuad = [202, OStack.pop(), OStack.pop(), OStack.pop()]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_one_par(p):
	'''one_par : CIR LP exp p_fill RP SC
| SQ LP exp p_fill RP SC'''
	if(p[1] == 'circle'):
		spCuad = [203, OStack.pop(),-1, -1]
	else:
		spCuad = [204, OStack.pop(), -1, -1]
	
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_poly(p):
	'''poly : POL LP idList p_fill RP SC'''
	spCuad = [205, OStack.pop(), -1, -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_lstrip(p):
	'''lstrip : LS LP idList RP SC'''
	spCuad = [206, OStack.pop(), -1, -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_idList(p):
	'''idList : ID'''
	declared_variables(p[1])
	type_variable(p[1], "list")
	OStack.push(p[1])	
#id debe ser tipo list not var

def p_p_arc(p):
	'''p_arc : ARC LP exp RP SC'''
	spCuad = [207, OStack.pop(), -1, -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1


def p_expresion(p):
	'''expresion : exp ex2 '''

def p_ex2(p):
	'''ex2 : ex3 exp 
| empty'''
	if(OpStack.size() > 0):
		if(OpStack.peek() == '>' or OpStack.peek() == '<' or OpStack.peek() == '<>' or OpStack.peek() == '=='):
			#checar tipos
			#tipo_resultante_ver()
			TStack.pop()
			TStack.pop()	
			global numQuad
			numQuad += 1
			tem = 'T'+ str(numQuad)
			spCuad = [OpStack.pop(), OStack.pop(), OStack.pop(), tem]
			quads.append(spCuad)	
			#meter temporal
			OStack.push(tem)
			TStack.push('tType')

def p_ex3(p):
	'''ex3 : LT 
| MT 
| D 
| SEQ'''
	OpStack.push(p[1])

def p_exp(p):
	'''exp : term exp2'''

def p_exp2(p):
	'''exp2 : exp3 exp 
| empty'''
	if(OpStack.size() > 0):
		if(OpStack.peek() == '+' or OpStack.peek() == '-'):
			#checar tipos
			#tipo_resultante_ver()
			
			global numQuad
			numQuad += 1
			h = avail.get_temp(OpStack.peek(), TStack.pop(), TStack.pop()) 
			tem = h[0]
			second = OStack.pop() 
			if(OpStack.pop() == '+'):
				spCuad = [102, OStack.pop(), second, tem] 		
			else:
				spCuad = [103, OStack.pop(), second, tem]
						
			quads.append(spCuad)	
			#meter temporal
			OStack.push(tem)
			TStack.push(h[1])
	
def p_exp3(p):
	'''exp3 : ADD 
| SUB'''
	OpStack.push(p[1])

def p_term(p):
	'''term : fact term2'''	

def p_term2(p):
	'''term2 : term3 term 
| empty'''
	if(OpStack.size() > 0):
		if(OpStack.peek() == '*' or OpStack.peek() == '/'):
			#checar tipos
			#tipo_resultante_ver(p[1])
			TStack.pop()
			TStack.pop()			
			global numQuad
			numQuad += 1
			tem = 'T'+ str(numQuad)
			second = OStack.pop() 
			if(OpStack.peek() == '*'):
				spCuad = [104, OStack.pop(), second, tem]
			else:
				spCuad = [105, OStack.pop(), second, tem]
			OpStack.pop()
			quads.append(spCuad)
			#meter temporal
			OStack.push(tem)
			TStack.push('tType')			

def p_term3(p):
	'''term3 : M 
| DIV'''
	OpStack.push(p[1])

def p_fact(p):
	'''fact : fact2 exp RP 
| fact4'''
	if(len(p) == 4):
		OpStack.pop()

def p_fact2(p):
	'''fact2 : LP '''
	OpStack.push(p[1])

def p_fact4(p):
	'''fact4 : valExp 
| ID'''	
	if(p[1] != None):
		declared_variables(p[1])
		TStack.push(type_variable(p[1], "var"))
		OStack.push(p[1])
					
def p_valExp(p):
	'''valExp : VALI 
| VALF  '''
	OStack.push(p[1])
	global vType
	a = re.compile('\d+\.\d+')
	if(a.match(p[1])):
		vType = "float"
	else:
		vType = "int"
	TStack.push(vType)


def p_rep(p):
	'''rep : RE exp block'''

def p_WID(p):
	'''WID : ID WID2'''
	if(idFunc == "ass"):
		declared_variables(p[1])
		if(OStack.size() > 0):
			#checar tipos
			#tipo_resultante_ver(p[1])			
			global numQuad
			numQuad += 1
			tem = 'T'+ str(numQuad)
			spCuad = [101, OStack.pop(), -1, p[1]]
			quads.append(spCuad)
			#meter temporal
			OStack.push(tem)
	else:
		if(p[1] not in proDict):
			print "Undeclared function", p[1]
			sys.exit(0)	
		else:
			if(len(proDict[p[1]]) != len(funCheck)):
				print "Error, function call, ", p[1]
			else:
				cont = 0
				for key in proDict[p[1]]:
					if(proDict[p[1]][key][0] != funCheck[cont]):
						
						print "Error, function call type miss match"
					cont += 1 

def p_WID2(p):
	'''WID2 : assigment
| funCall'''

def p_assigment(p):
	'''assigment : EQ tipeAss'''
	global idFunc
	idFunc = "ass"

def p_tipeAss(p):
	'''tipeAss : varAss
| listAss'''

def p_varAss(p):
	'''varAss : exp SC'''

def p_funCall(p):
	'''funCall : LP func2 RP SC'''
	global idFunc
	idFunc = "func"
	
def p_func2(p):
	'''func2 : func4 func3
| empty'''

def p_func3(p):
	'''func3 : C func4 func3
| empty'''

def p_func4(p):
	'''func4 : exp '''
	funCheck.append(vType)

def p_list(p):
	'''list : L type ID prelistAss'''
	if p[3] in ht:
		print "Existing var, ", p[3]
	else:
		ht[p[3]] = [vType, "list"]

def p_prelistAss(p):
	'''prelistAss : EQ listAss
| SC'''

def p_listAss(p):
	'''listAss : LB lista3 RB SC'''

def p_lista2(p):
	'''lista2 : val 
| ID'''

def p_lista3(p):
	'''lista3 : lista2 li4'''

def p_li4(p):
	'''li4 : C lista2 li4
| empty'''

def p_lab(p):
	'''lab : LA LP stExp lab2 RP SC'''
	spCuad = [208, OStack.pop(), -1, -1]
	quads.append(spCuad)
	global numQuad 
	numQuad += 1

def p_lab2(p):
	'''lab2 : ADD stExp lab2
| empty'''

def p_stExp(p):
	'''stExp : STR
| exp'''

def p_condition(p):
	'''condition : IF LP expresion RP block con2'''

def p_con2(p):
	'''con2 : empty  
| ELSE block'''

def p_block(p):
	'''block : LB block3 RB'''

def p_block3(p):
	'''block3 : block2 block3
| empty '''

def p_figure(p):
	'''figure : rect
| tria
| poly
| lstrip
| one_par
| p_arc'''

def p_pen(p):
	'''pen : colors 
| p_width  
| move 
| position 
| penwrite '''

def p_block2(p):
	'''block2 : figure 
| condition 
| pen 
| lab 
| list 
| WID
| rep'''

def p_empty(p):
    '''empty : '''

def declared_variables(p):
	global vType
	if(p != None):
		if(p not in ht):
			if("globals" in proDict):
				if(p not in proDict["globals"]):
					print "Undeclared variable. ", p
					sys.exit(0)
				else:
					vType = proDict["globals"][p][0]
			else:
				print "Undeclared variable. ", p
				sys.exit(0)
		else:
			vType = ht[p][0]
# Error rule for syntax errors

def type_variable(p, type_v):
	if p in ht:
		if(ht[p][1] != type_v):
			print "Type miss match.", type_v, " " ,p
			sys.exit(0)
		else:
			return ht[p][0]
	else:
		if("globals" in proDict):
			if(proDict["globals"][p][1] != type_v):
				print "Type miss match.", type_v, " " , p
				sys.exit(0)
			else:
				return proDict["globals"][p][0]



	

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
