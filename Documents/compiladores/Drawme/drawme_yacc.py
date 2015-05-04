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
aType = None
proDict = dict()
const = dict()
idFunc = None
avail = avail()
funCheck = [] #Check function parameters
toFile = ''
int_qty = 2000
float_qty = 3000
str_qty = 1000
const_int_qty = 40000
const_float_qty = 41002
const_str_qty = 42000
empty = False
vD = 0
offset = 0
ID = ''
MDim = False
DT = False
DTQty = 0
pointer = False
pointDir = 0

def p_prog(p):
	'''prog : PR p2 p3 main mainVDir block'''
	print ht
	temp = [(str_qty-1000), (int_qty-2000), (float_qty-3000)]
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
	avail.main()

def p_p3(p):
	'''p3 : functions p3
| empty'''

def p_globals(p):
	'''globals : glob vars'''
	global str_qty, int_qty, float_qty
	block_dir(ht, 1)
	vaDict = dict(ht)
	temp = [vaDict, (str_qty-1000), (int_qty-2000), (float_qty-3000)]
	temp.extend(avail.get_temp_dirs())
	proDict["globals"] = temp
	ht.clear()
	str_qty = 1000
	int_qty = 2000
	float_qty = 3000

def p_glob(p):
	'''glob : GL'''
	avail.setblock(1)
	

def p_functions(p): 
	'''functions : fun2 funVDir block'''	
	
	temps = avail.get_temp_dirs()
	proDict[avail.getScope()][5] = temps[0]
	proDict[avail.getScope()][6] = temps[1]
	proDict[avail.getScope()][7] = temps[2]
	proDict[avail.getScope()][8] = temps[3]
	ht.clear()
	avail.function_end()
	

def p_funVDir(p):
	'''funVDir : vars '''
	#print "function    ", ht, '\n'
	block_dir(ht, 3)
	global str_qty, int_qty, float_qty, idFunc
	proDict[idFunc][2] = (str_qty-1000)
	proDict[idFunc][3] = (int_qty-2000)
	proDict[idFunc][4] = (float_qty-3000)
	str_qty = 1000
	int_qty = 2000
	float_qty = 3000

def p_fun2(p):
        '''fun2 : funBlock fID LP fun3 RP'''
	vaDict = dict(funPar)
	global str_qty, int_qty, float_qty, idFunc
	idFunc = avail.getScope()
	temp = [vaDict, avail.getfuncQuad(), (str_qty-2000), (int_qty-2000), (float_qty-3000), 0, 0, 0, 0]
	proDict[avail.getScope()] = temp
	qty = proDict["globals"][3] + 1
	proDict["globals"][0][avail.getScope()] = ["float", 'func', 13000 + qty]
	proDict["globals"][3] = qty
	print proDict["globals"]
	funPar.clear()

def p_fID(p):
	'''fID : ID '''
	avail.setScope(p[1])

def p_funBlock(p):
        '''funBlock : FUN tp'''
	avail.setfuncQuad()
	avail.setblock(3)

def p_tp(p):
        '''tp : VD 
| type'''
	global vType
	if(p[1] == 'void'):
		vType = p[1]
	avail.setRT(vType)

def p_fun3(p):
	'''fun3 : fun5 fun4
| empty'''
	

def p_fun4(p):
	'''fun4 : C fun5 fun4  
| empty'''

def p_fun5(p):
	'''fun5 : type arr ID arrDim'''
	global pointer, pointDir
	if pointer:
		pDir = avail.get_temp_point()
		if p[3] in ht:
			print "Existing var, ", p[3]
			sys.exit(0)
		else:
			ht[p[3]] = [aType, "point", (pDir-30000)]
			if pointDir > 0:
				ht[p[3]].append(pointDir)
		pointer = False
	else:
		save_var(p[3])
	funPar[p[3]] = [vType, "var", (ht[p[3]][2]+30000)]

def p_arr(p):
	'''arr : P
| empty '''
	global pointer
	if p[1] == '&':
		pointer = True
	else:
		pointer = False	

def p_arrDim(p):
	'''arrDim : LC exp RC 
| empty'''
#dir array
	if len(p) > 2:
		global pointDir
		exp = avail.OStack_pop()
		for value, vDir in const.iteritems():
			if exp == vDir :
				pointDir = value
		

def p_vars(p): 
	'''vars : V var2 
| empty'''

def p_var2(p):
        '''var2 : type var3 SC var2
| empty'''

def p_var3(p):
	'''var3 : varSave var5 var4 var33 '''

def p_var33(p):
	'''var33 : C varSave var5 var4 var33 
| empty '''

def p_varSave(p):
	'''varSave : ID '''
	save_var(p[1])
	global vD
	vD = var_dir(p[1]) + (avail.getblock() * 10000)
	avail.IDStack_push(p[1])

def p_var4(p):
        '''var4 : EQ var6 
| empty'''
	if len(p) != 3:
		avail.DStack_pop()

def p_var5(p):
	'''var5 : LC var51
| LB var52
| empty'''
	if(len(p) < 3):
		avail.DStack_push(False)

def p_var6(p):
	'''var6 : exp
| LB LP exp C exp RP var61 RB
| LC exp var62 RC'''
#whe declaring variables and you have an assing you have to check the type of assignation
	global vD, vType, DTQty
	if len(p) == 2: 
#if it's a normal asign k=0 or k=j, i
		if(avail.OStack_peek() < 10000):
		#if the variable that is being assigned is from that bolck the correct direction is needed
			dV = avail.OStack_pop() + (avail.getblock() * 10000)
			avail.OStack_push(dV)
		avail.assig(vD)
	elif(len(p) == 5):
	#array
		if(avail.DStack_pop()):
			ID = avail.IDStack_pop()
			print ID
			vDim = dim(ID)
			while DTQty >= 0 :
				avail.dimP(vD, DTQty, vDim)
				DTQty -= 1
			DTQty = 0
		else:
			print "error, missmatch types"
	else:
	#matrix
		print "MATRIX", p[1]
		if not avail.DStack_pop():
			print "error, missmatch types"
		else:
			ID = avail.IDStack_pop()
			vDim = dim(ID)
			while DTQty >= 0:
				print "while", DTQty
				avail.dimTP(vD, DTQty, vDim)
				DTQty -= 1
			DTQty = 0
			

def p_var61(p):
	'''var61 : C LP exp C exp RP var61
| empty'''
	if(len(p) > 2):
		global DTQty
		DTQty += 1

def p_var62(p):
	'''var62 : C exp var62
| empty'''
	if(len(p) > 2):
		global DTQty
		DTQty += 1

def p_var51(p):
	'''var51 : exp RC '''
#dir array
	global aType, int_qty, float_qty
	ID = avail.IDStack_pop()
	exp = avail.OStack_pop()
	for value, vDir in const.iteritems():
		if exp == vDir :
			if aType == 'int':
				int_qty += int(value) + 1
			else:
				float_qty += int(value) + 1
			ht[ID].append(value)
	avail.DStack_push(True)
	avail.IDStack_push(ID)
	
def p_var52(p):
#dir matrix
	'''var52 : exp RB'''
	global aType, int_qty, float_qty
	ID = avail.IDStack_pop()
	exp = avail.OStack_pop()
	print "DIR MATRIX "
	for value, vDir in const.iteritems():
		if exp == vDir :
			if aType == 'int':
				int_qty += (int(value)+1)*2 
			else:
				float_qty += (int(value)+1)*2 
			print "DIR MATRIX ", (int(value)+1)*2 
			ht[ID].append((int(value)+1)*2 )
	avail.DStack_push(True)
	avail.IDStack_push(ID)
				

def p_type(p):
	'''type : INT 
| FLOAT  '''
	global vType, aType
	vType = p[1]
	aType = p[1]

#def p_val(p):
#	'''val : VALI 
#| VALF  '''
#	if p[1] not in const:
#		global const_int_qty, const_float_qty
#		a = re.compile('\d+\.\d+')
#		if(a.match(p[1])):
#			const[p[1]] = const_float_qty
#			const_float_qty += 1
#		else:
#			const[p[1]] = const_int_qty
#			const_int_qty += 1

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
	'''penwrite : PENX LP exp RP SC 
| PENY LP exp RP SC
| PENU LP exp RP SC
| PEND LP exp RP SC
| PENL LP exp RP SC
| PENR LP exp RP SC'''
	if(p[1] == 'penX'):
		spCuad = 308
	elif p[1] == 'penY':
		spCuad = 309
	elif p[1] == 'penUp':
		spCuad = 310
	elif p[1] == 'penDown':
		spCuad = 311
	elif p[1] == 'penLeft':
		spCuad = 312
	else:
		spCuad = 313
	avail.append_quad_one(spCuad)

def p_move(p):
	'''move : LI mueve2 '''
	avail.append_quad_two(305)

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
	avail.append_quad_two(205)

def p_lstrip(p):
	'''lstrip : LS LP idList RP SC'''
	avail.append_quad_two(206)

def p_idList(p):
	'''idList : ID'''
	declared_variables(p[1])
	dimention = dim(p[1])
	if dim(p[1]) == -1:
		print "dimention error"
		sys.error(0)
	avail.OStack_push(var_dir(p[1]))
	avail.OStack_push(dimention)
#id debe ser tipo list not var

def p_p_arc(p):
	'''p_arc : ARC LP exp p_fill RP SC'''
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
| SEQ
| LET
| MET'''
	avail.OpStack_push(p[1])

def p_exp(p):
	'''exp : term exp2'''
	global empty
	empty = False

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
| factID fact5'''
	if(len(p) == 3):
		ID = avail.IDStack_pop()
		MDim = avail.DStack_pop()
		if(MDim):		
			pointer = avail.OStack_pop()
		declared_variables(ID)
		avail.TStack_push(type_variable(ID, "var"))
		avail.OStack_push(var_dir(ID))
		if(MDim):
			print "MDIM", dim(ID)
			avail.dim(dim(ID), pointer)
		if not MDim:
			if avail.DStack_pop():
				print avail.OStack_pop()
				avail.TStack_pop()
				

def p_factID(p):
	'''factID : ID '''
	avail.setFuncScope(p[1])
	avail.IDStack_push(p[1])

def p_fact5(p):
	'''fact5 : LC exp RC
| LB exp RB
| funCall
| empty'''
#check if its a function, an array, matrix or a simple var.
	global empty	
	if(len(p) == 4):
		avail.DStack_push(True)
		if p[1] == '[':
			avail.DStack_push(True)
		else:
			global DT
			DT = True
			avail.DStack_push(False)
	elif not empty:
		avail.DStack_push(True)
		avail.DStack_push(False)
	else:
		avail.delFuncScope()
		avail.DStack_push(False)
		avail.DStack_push(False)

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
	avail.rep_jump(const['1'], const['0'])

def p_rep3(p):
	'''rep3 : valExp
| ID'''
	print "BAH", p[1]
	if p[1] != None:
		declared_variables(p[1])
		avail.TStack_push(type_variable(p[1], "var"))
		avail.OStack_push(var_dir(p[1]))
	avail.rep()
	

def p_WID(p):
	'''WID : factID fact5 WID2'''
	ID = avail.IDStack_pop()
	if(idFunc == "ass"):
		#avail.delFuncScope()
		TDim = avail.DStack_pop()		
		declared_variables(ID)
		if(avail.DStack_pop()):
			print "THREE" ,  avail.OStack_peek()
			if(TDim):
				par = avail.OStack_pop()
				par2 = avail.OStack_pop()
				avail.OStack_push(par)
				avail.TStack_push(type_variable(ID, "var"))
				avail.OStack_push(var_dir(ID))
				avail.OStack_push(par2)
				avail.dim(dim(ID), avail.OStack_pop())
				avail.assig(avail.OStack_pop())
			else:
				par = avail.OStack_pop()
				par2 = avail.OStack_pop()
				par3 = avail.OStack_pop()
				avail.OStack_push(par)
				avail.OStack_push(par2)
				avail.TStack_push(type_variable(ID, "var"))
				avail.OStack_push(var_dir(ID))
				avail.OStack_push(par3)
				avail.dimT(dim(ID), avail.OStack_pop())
				avail.assig(avail.OStack_pop())
				avail.assig(avail.OStack_pop())
		else:
			avail.assig(var_dir(ID))
	else:
		if(ID not in proDict):
			print "Undeclared function", ID
			sys.exit(0)	
		else:
			if((len(proDict[ID][0])) != len(funCheck)):
				print funCheck
				print "Error, function call, ", ID
				sys.error(0)
			else:
				cont = 0
				for key in proDict[ID][0]:
					if(proDict[ID][0][key][0] != funCheck[cont]):
						
						print "Error, function call type miss match"
						sys.error(0)
					cont += 1 
	funCheck[:] = []

def p_WID2(p):
	'''WID2 : assigment
| SC'''

def p_assigment(p):
	'''assigment : EQ tipeAss'''
	global idFunc
	idFunc = "ass"

def p_tipeAss(p):
	'''tipeAss : exp SC
| listAss '''

def p_funCall(p):
	'''funCall : funEra func2 RP '''
	global idFunc, empty
	idFunc = "func"
	print "funCall", avail.getFuncScope()
	if avail.getFuncScope() not in proDict:
		print "Error, function doesn't exist"
		sys.exit(0)
	print "funCall", proDict[avail.getFuncScope()][0]
	avail.function_param(proDict[avail.getFuncScope()][0])
	vDir = 10000
	qty = proDict["globals"][6]
	vDir += 6000 + qty
	proDict["globals"][6] = qty + 1
	avail.call_function_end(proDict[avail.getFuncScope()][1], var_dir(avail.getFuncScope()), vDir)
	empty = False

def p_funEra(p):
	'''funEra : LP '''
	avail.call_function(avail.getScope())

def p_func2(p):
	'''func2 : func4 func3
| empty'''

def p_func3(p):
	'''func3 : C func4 func3
| empty'''

def p_func4(p):
	'''func4 : exp '''
	funCheck.append(vType)
	
def p_listAss(p):
	'''listAss : LB exp C exp RB SC'''
	global DT
	if(not DT):
		print "Dimension error"
		sys.error(0)
	else:
		DT = False

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

def p_rt(p):	
	'''rt : RT rtE SC'''
	if(avail.getScope() == 'main'):
		print "ERROR, no return in main"

def p_rtE(p):
	'''rtE : exp 
| empty'''
	global empty, vType
	
	print "RETURN", avail.getScope()
	avail.function_return(empty, var_dir(avail.getScope()))
	empty = False

def p_label(p):
	'''label : LA LP STR RP SC'''
	global str_qty, const_str_qty
	print p[3]
	sub = 1
	start = str_qty - 1000
	strDir = str_qty + (avail.getblock() * 10000)
	word = p[3]
	while sub < len(word)-1:
		if word[sub] not in const:
			const[word[sub]] = const_str_qty
			const_str_qty += 1
		spCuad = ['101',  const[word[sub]], -1, (str_qty + (avail.getblock() * 10000))]
		str_qty += 1
		avail.append_quad(spCuad)
		print sub
		sub += 1
	finish = str_qty - 1000	-1
	print "FIJN", finish
	spCuad = ['208',  strDir , start, finish]
	avail.append_quad(spCuad)

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
| p_arc
| label'''

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
| WID
| rep
| rt'''

def p_empty(p):
	'''empty : '''
	global empty
	empty = True

def save_var(var):
	global aType
	if var in ht:
		print "Existing var, ", var
		sys.exit(0)
	else:
		if aType == "int":
			global int_qty
			ht[var] = [aType, "var", int_qty]
			int_qty += 1 
		else:
			global float_qty
			ht[var] = [aType, "var", float_qty] 
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
		return ht[p][0]
	else:
		if "globals" in proDict:
			return proDict["globals"][0][p][0]

def var_dir(p):
	if p in ht:
		return ht[p][2]
	else:
		if "globals" in proDict:
			return proDict["globals"][0][p][2]

def dim(p):
	if p in ht:
		try:
			return ht[p][3]
		except IndexError:
			return -1
	else:
		if "globals" in proDict:
			try:
				return proDict["globals"][0][p][3]
			except IndexError:
				return -1

def dict_to_string(convDict):
	s = ''
	for key in convDict:
		info = convDict[key]
		if(key == 'main' or key == 'globals'):
			s += str(key) + ' ' + str(info[0]) + ' ' + str(info[1]) + ' ' + str(info[2]) + ' ' + str(info[3]) + ' ' + str(info[4]) + ' ' + str(info[5]) + ' ' + str(info[6]) + '\n'
		else:
			s += str(key) + ' ' + str(info[2]) + ' ' + str(info[3]) + ' ' + str(info[4]) + ' ' + str(info[5]) + ' ' + str(info[6]) + ' ' + str(info[7]) + ' ' + str(info[8]) + '\n'
	s += '%%' + '\n'
	return s

def dict_to_string_cons(convDict):
	s = ''
	for key in convDict:
		info = convDict[key]
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
		const['1'] = const_int_qty
		const_int_qty += 1
	if 0 not in const:		
		const['0'] = const_int_qty
		const_int_qty += 1
	if 2 not in const:		
		const['2'] = const_int_qty
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
		toFile += str(const_int_qty - 40000) + " " + str(const_float_qty - 41000) + " " + str(const_str_qty - 42000) + '\n'	
		toFile += str(dict_to_string_cons(const))
		toFile += str(dict_to_string(proDict))
		print proDict
		quads_to_file()
		#print toFile
		wFile = open('program.txt', 'w+')
		wFile.write(toFile)
		wFile.close()
else:
    print "):"
