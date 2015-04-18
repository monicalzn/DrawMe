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
const = dict()
scope = None
idFunc = None
avail = avail()
funCheck = [] #Check function parameters
global toFile
toFile = ''
int_qty = 2000
float_qty = 3000
const_int_qty = 40004
const_float_qty = 41002

def p_prog(p):
	'''prog : PR p2 p3 main mainVDir block'''
	print ht
	temp = [(int_qty-2000), (float_qty-3000)]
	temp.extend(avail.get_temp_dirs())
	proDict["main"] = temp
	if("globals" in proDict):
		temp = proDict["globals"]
		temp.pop(0)
		proDict["globals"] = temp
	spCuad = ['ENDPROG', -1, -1, -1]
	avail.append_quad(spCuad)
	#print proDict
	#print const
	#avail.print_quads()

def p_main(p):
	'''main : MAIN '''
	avail.main_goto()
	avail.setblock(2)

def p_mainVDir(p):
	'''mainVDir : vars'''
	block_dir(ht, 2)

def p_p2(p):
	'''p2 : globals 
| empty'''
	avail.colors()
	avail.main()

def p_p3(p):
	'''p3 : functions p3
| empty'''

def p_globals(p):
	'''globals : glob vars'''
	global int_qty, float_qty
	block_dir(ht, 1)
	vaDict = dict(ht)
	temp = [vaDict, (int_qty-2000), (float_qty-3000)]
	temp.extend(avail.get_temp_dirs())
	proDict["globals"] = temp
	ht.clear()
	int_qty = 2000
	float_qty = 3000

def p_glob(p):
	'''glob : GL'''
	avail.setblock(1)
	

def p_functions(p): 
	'''functions : fun2 DP funVDir block'''	
	avail.function_begin()	
	temps = avail.get_temp_dirs()
	proDict[avail.getScope()][3] = temps[0]
	proDict[avail.getScope()][4] = temps[1]
	proDict[avail.getScope()][5] = temps[2]
	ht.clear()
	avail.function_end()
	

def p_funVDir(p):
	'''funVDir : vars '''
	#print "function    ", ht, '\n'
	block_dir(ht, 3)
	global int_qty, float_qty, idFunc
	proDict[idFunc][1] = (int_qty-2000)
	proDict[idFunc][2] = (float_qty-3000)
	int_qty = 2000
	float_qty = 3000

def p_fun2(p):
        '''fun2 : funBlock ID LP fun3 RP'''
	vaDict = dict(funPar)
	avail.setScope(p[2])
	global int_qty, float_qty, idFunc
	idFunc = p[2]
	temp = [vaDict, (int_qty-2000), (float_qty-3000), 0, 0, 0]
	proDict[p[2]] = temp
	avail.function_param(vaDict)
	funPar.clear()
	

def p_funBlock(p):
        '''funBlock : FUN '''
	avail.setblock(3)

def p_fun3(p):
	'''fun3 : fun5 fun4
| empty'''
	

def p_fun4(p):
	'''fun4 : C fun5 fun4  
| empty'''

def p_fun5(p):
	'''fun5 : type ID '''
	save_var(p[2])
	funPar[p[2]] = [vType, "var", (ht[p[2]][2]+30000)]
	

def p_vars(p): 
	'''vars : V var2 var5
| empty'''

def p_var2(p):
        '''var2 : type var3 SC var2
| empty'''

def p_var3(p):
	'''var3 : ID var4 var33 '''
	save_var(p[1])

def p_var33(p):
	'''var33 : C ID var4 var33 
| empty '''
	if(len(p) == 5):
		save_var(p[2])

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
	if p[1] not in const:
		global const_int_qty, const_float_qty
		a = re.compile('\d+\.\d+')
		if(a.match(p[1])):
			const[p[1]] = const_float_qty
			const_float_qty += 1
		else:
			const[p[1]] = const_int_qty
			const_int_qty += 1

def p_position(p):
	'''position : PENP LP exp C exp RP SC'''
	avail.append_quad_two(307)

def p_colors(p):
	'''colors : PENC LP exp C exp C exp RP SC 
| SETC LP exp C exp C exp RP SC 
| BACO LP exp C exp C exp RP SC '''
	if(p[1] == 'penColor'):
		fun = 301
	elif(p[1] == 'setColor'):
		fun = 302
	else:
		fun = 303
	avail.append_quad_three(fun)


def p_p_width(p):
	'''p_width : PENW LP exp RP SC '''
	avail.append_quad_one(304)

def p_penwrite(p):
	'''penwrite : PENU SC 
| PEND SC'''
	if(p[1] == 'penUp'):
		spCuad = [308, -1, -1, -1]
	else:
		spCuad = [309, -1, -1, -1]
	avail.append_quad(spCuad)

def p_move(p):
	'''move : F mueve2
| B mueve2'''

def p_mueve2(p):
	'''mueve2 : LP exp C A exp RP SC'''

def p_rect(p):
	'''rect : REC LP exp C exp p_fill RP SC'''
	avail.append_quad_two(201)

def p_p_fill(p):
	'''p_fill : C FILL 
| empty'''
	if(len(p) == 3):
		spCuad = [209, -1, -1, 1]
	else:
		spCuad = [209, -1, -1, -1]
	avail.append_quad(spCuad)

def p_tria(p):
	'''tria : TRI LP LC exp C exp RC C LC exp C exp RC C LC exp C exp RC p_fill RP SC'''
	avail.append_quad_tri(202)

def p_one_par(p):
	'''one_par : CIR LP exp p_fill RP SC
| SQ LP exp p_fill RP SC'''
	if(p[1] == 'circle'):
		spCuad = 203
	else:
		spCuad = 204
	avail.append_quad_one(spCuad)

def p_poly(p):
	'''poly : POL LP idList p_fill RP SC'''
	avail.append_quad_one(205)

def p_lstrip(p):
	'''lstrip : LS LP idList RP SC'''
	avail.append_quad_one(206)

def p_idList(p):
	'''idList : ID'''
	declared_variables(p[1])
	type_variable(p[1], "list")
	avail.OStack_push(var_dir(p[1]))	
#id debe ser tipo list not var

def p_p_arc(p):
	'''p_arc : ARC LP exp RP SC'''
	avail.append_quad_one(207)

def p_expresion(p):
	'''expresion : exp ex2 '''

def p_ex2(p):
	'''ex2 : ex3 exp 
| empty'''
	avail.expression()

def p_ex3(p):
	'''ex3 : LT 
| MT 
| D 
| SEQ'''
	avail.OpStack_push(p[1])

def p_exp(p):
	'''exp : term exp2'''

def p_exp2(p):
	'''exp2 : exp4 exp3 exp 
| exp4 empty'''

def p_exp4(p):
	'''exp4 : empty'''
	avail.add_sub()

def p_exp3(p):
	'''exp3 : ADD 
| SUB'''
	avail.OpStack_push(p[1])

def p_term(p):
	'''term : fact term2'''	

def p_term2(p):
	'''term2 : term4 term3 term 
| term4 empty'''	

def p_term4(p):
	'''term4 : empty'''
	avail.mul_div()	

def p_term3(p):
	'''term3 : M 
| DIV'''
	avail.OpStack_push(p[1])

def p_fact(p):
	'''fact : fact2 exp RP 
| fact4'''
	if(len(p) == 4):
		avail.OpStack_pop()

def p_fact2(p):
	'''fact2 : LP '''
	avail.OpStack_push(p[1])

def p_fact4(p):
	'''fact4 : valExp 
| ID'''	
	if(p[1] != None):
		declared_variables(p[1])
		avail.TStack_push(type_variable(p[1], "var"))
		avail.OStack_push(var_dir(p[1]))
					
def p_valExp(p):
	'''valExp : VALI 
| VALF  '''
	a = re.compile('\d+\.\d+')
	if p[1] not in const:
		global const_int_qty, const_float_qty
		if(a.match(p[1])):
			const[p[1]] = const_float_qty
			const_float_qty += 1
		else:
			const[p[1]] = const_int_qty
			const_int_qty += 1
	avail.OStack_push(const[p[1]])
	global vType
	if(a.match(p[1])):
		vType = "float"
	else:
		vType = "int"
	avail.TStack_push(vType)

def p_rep(p):
	'''rep : RE rep3 block'''
	avail.rep_jump(const[1], const[0])

def p_rep3(p):
	'''rep3 : exp'''
	avail.rep()
	

def p_WID(p):
	'''WID : ID WID2'''
	if(idFunc == "ass"):
		declared_variables(p[1])
		avail.assig(var_dir(p[1]))
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
	
	avail.call_function_end(idFunc)

def p_func3(p):
	'''func3 : C func4 func3
| empty'''
	avail.function_param(funPar)

def p_func4(p):
	'''func4 : exp '''
	funCheck.append(vType)
	avail.call_function(idFunc)
	
def p_list(p):
	'''list : L type ID prelistAss'''
	if p[3] in ht:
		print "Existing var, ", p[3]
	else:
		ht[p[3]] = [vType, "list", 0]

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
	avail.append_quad_one(208)

def p_lab2(p):
	'''lab2 : ADD stExp lab2
| empty'''

def p_stExp(p):
	'''stExp : STR
| exp'''

def p_condition(p):
	'''condition : IF LP expresion condRP block con2'''
	avail.condition_start()

def p_condRP(p):
	'''condRP : RP'''
	avail.condition()
				

def p_con2(p):
	'''con2 : empty  
| con3 block'''

def p_con3(p):
	'''con3 : ELSE '''
	avail.condition_else()
	

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

def save_var(var):
	if var in ht:
		print "Existing var, ", var
	else:
		if vType == "int":
			global int_qty
			ht[var] = [vType, "var", int_qty]
			int_qty += 1 
		else:
			global float_qty
			ht[var] = [vType, "var", float_qty] 
			float_qty += 1

def block_dir(blockDict, block):
	for key in blockDict:
		info = blockDict[key]
		info[2] = info[2] + (block * 10000)
		blockDict[key] = info

def declared_variables(p):
	global vType
	if(p != None):
		if(p not in ht):
			if("globals" in proDict):
				if(p not in proDict["globals"][0]):
					print "Undeclared variable. ", p
					sys.exit(0)
				else:
					vType = proDict["globals"][0][p][0]
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
			if(proDict["globals"][0][p][1] != type_v):
				print "Type miss match.", type_v, " " , p
				sys.exit(0)
			else:
				return proDict["globals"][0][p][0]

def var_dir(p):
	if p in ht:
		return ht[p][2]
	else:
		if "globals" in proDict:
			return proDict["globals"][0][p][2]

def dict_to_string(convDict):
	s = ''
	for key in convDict:
		info = convDict[key]
		if(key == 'main' or key == 'globals'):
			s += str(key) + ' ' + str(info[0]) + ' ' + str(info[1]) + ' ' + str(info[2]) + ' ' + str(info[3]) + ' ' + str(info[4]) + '\n'
		else:
			s += str(key) + ' ' + str(info) + '\n'
	s += '%%' + '\n'
	return s

def quads_to_file():
	global toFile
	quads = avail.get_quads()
	for q in quads:
		toFile += str(q[0]) + " " + str(q[1]) + " " + str(q[2]) + " " + str(q[3]) + " " + '\n'

def one():
	global const_int_qty
	if 1 not in const:
		const[1] = const_int_qty
		const_int_qty += 1
	if 0 not in const:		
		const[0] = const_int_qty
		const_int_qty += 1
def p_error(p):
	print "Syntax error in input!", p.type

# Build the parser
parser = yacc.yacc()

if(len(sys.argv) > 1):
	if sys.argv[1] == "-f":
		f = open(sys.argv[2], "r")
		one()
		s = f.readlines()
		string = ""
		for line in s:
			string += line
		result = parser.parse(string)
		toFile += str(const_int_qty - 40000) + " " + str(const_float_qty - 41000) + '\n'	
		toFile += str(dict_to_string(const))
		toFile += str(dict_to_string(proDict))
		quads_to_file()
		#print toFile
		wFile = open('program.txt', 'w+')
		wFile.write(toFile)
		wFile.close()	
else:
    print "):"
