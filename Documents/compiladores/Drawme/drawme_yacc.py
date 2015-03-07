import ply.yacc as yacc
import drawme_lex 
import sys

from has import HashTable

tokens = drawme_lex.tokens
ht = HashTable()
word = "l"
vType = "nada"

def p_prog(p):
	'''prog : PR p2 p3 MAIN vars block'''

def p_p2(p):
	'''p2 : globals 
| empty'''
	ht.put(word, 1)

def p_p3(p):
	'''p3 : functions p3
| empty'''

def p_globals(p):
	'''globals : GL vars'''

def p_functions(p): 
	'''functions : FUN ID fun2 DP vars block SC'''

def p_fun2(p):
        '''fun2 : LP fun3'''

def p_fun3(p):
	'''fun3 : type ID fun4 RP
| RP'''

def p_fun4(p):
	'''fun4 : C type ID fun4  
| empty'''

def p_vars(p): 
	'''vars : V var2 var5
| empty'''
	print 1

def p_var2(p):
        '''var2 : type var3 SC var2
| empty'''
	print 2

def p_var3(p):
	'''var3 : ID var4 var33 '''
	print 3, vType

def p_var33(p):
	'''var33 : C ID var4 var33 
| empty '''
	print 4

def p_var4(p):
        '''var4 : EQ exp 
| empty'''
	print 5

def p_var5(p):
	'''var5 : list var5
| empty'''
	print 6

def p_type(p):
	'''type : INT 
| FLOAT  '''
	global vType
	vType = p[1]
	print 7

def p_val(p):
	'''val : VALI 
| VALF  '''

def p_position(p):
	'''position : PENP LP exp C exp RP SC'''

def p_colors(p):
	'''colors : PENC colors2 
| SETC colors2 
| BACO colors2 '''

def p_colors2(p):
	'''colors2 : LP exp C exp C exp RP SC'''

def p_p_width(p):
	'''p_width : PENW LP exp RP SC '''

def p_penwrite(p):
	'''penwrite : PENU SC 
| PEND SC'''

def p_move(p):
	'''move : F mueve2
| B mueve2'''

def p_mueve2(p):
	'''mueve2 : LP exp C A exp RP SC'''

def p_rect(p):
	'''rect : REC LP exp C exp p_fill RP SC'''

def p_p_fill(p):
	'''p_fill : C FILL 
| empty'''

def p_tria(p):
	'''tria : TRI LP exp C exp C exp p_fill RP SC'''

def p_one_par(p):
	'''one_par : CIR opar2 
| SQ opar2'''

def p_opar2(p):
	'''opar2 : LP exp p_fill RP SC'''

def p_poly(p):
	'''poly : POL LP idList p_fill RP SC'''

def p_lstrip(p):
	'''lstrip : LS LP idList RP SC'''

def p_idList(p):
	'''idList : list 
| ID'''
#id debe ser tipo list not var

def p_p_arc(p):
	'''p_arc : ARC LP exp RP SC'''


def p_expresion(p):
	'''expresion : exp ex2 '''

def p_ex2(p):
	'''ex2 : ex3 exp 
| empty'''

def p_ex3(p):
	'''ex3 : LT 
| MT 
| D 
| SEQ'''

def p_exp(p):
	'''exp : term exp2'''
#/* poper saca + o - */

def p_exp2(p):
	'''exp2 : exp3 exp 
| empty'''

def p_exp3(p):
	'''exp3 : ADD 
| SUB'''
#/*mete a poper*/

def p_term(p):
	'''term : fact term2'''
#/*une a poper * o / */

def p_term2(p):
	'''term2 : term3 term 
| empty'''

def p_term3(p):
	'''term3 : M 
| DIV'''
#/*mete a poper*/

def p_fact(p):
	'''fact : LP exp RP 
| fact2'''

def p_fact2(p):
	'''fact2 : fact3 fact4'''

def p_fact3(p):
	'''fact3 : ADD 
| SUB 
| empty'''

def p_fact4(p):
	'''fact4 : val 
| ID'''

def p_rep(p):
	'''rep : RE exp block'''

def p_WID(p):
	'''WID : ID WID2'''

def p_WID2(p):
	'''WID2 : assigment
| funCall'''

def p_assigment(p):
	'''assigment : EQ tipeAss'''

def p_tipeAss(p):
	'''tipeAss : varAss
| listAss'''

def p_varAss(p):
	'''varAss : exp SC'''

def p_funCall(p):
	'''funCall : LP func2 RP SC'''

def p_func2(p):
	'''func2 : exp func3 
| empty'''

def p_func3(p):
	'''func3 : C exp func3
| empty'''

def p_list(p):
	'''list : L type ID prelistAss'''

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
