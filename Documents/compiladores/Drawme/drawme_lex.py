import ply.lex as lex

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'program' : 'PR',
   'var' : 'V',
   'main' : 'MAIN',
   'int' : 'INT',
   'float' : 'FLOAT',
   'global' : 'GL',
   'function': 'FUN',
   'penwidth':'PENW',
   'penpos':'PENP',
   'pencolor':'PENC',
   'penup': 'PENU',
   'pendown':'PEND',
   'setcolor':'SETC',
   'backgroundcolor' : 'BACO',
   'forward':'F',
   'rectangle' :'REC',
   'fill' :'FILL',
   'triangle' :'TRI',
   'circle' : 'CIR',
   'square' : 'SQ',
   'polygon' : 'POL',
   'angle' : 'A',
   'arc' : 'ARC',
   'linestrip' : 'LS',
   'back' : 'B',
   'angle' : 'A',
   'repeat' : 'RE',
   'list' : 'L',
   'label' : 'LA'
}

#List of token name.
tokens = [
	'LB', 'RB', 'DP', 'C', 'LP', 'RP', 'EQ', 'VALI', 'VALF', 'SEQ', 'D', 'MT', 'LT', 'ADD', 'SUB', 'M', 'DIV', 'STR', 'SC', 'ID'
	] + list(reserved.values())

t_ignore 	= ' \t\n\r'
t_EQ     	= r'='
t_MT      	= r'>'
t_LT      	= r'<'
t_D             = r'<>'
t_ADD     	= r'\+'
t_SUB    	= r'-'
t_M     	= r'\*'
t_DIV  		= r'/'
t_SC    	= r';'
t_DP 		= r':'
t_C     	= r'\,'
t_LB    	= r'\{'
t_RB    	= r'\}'
t_LP    	= r'\('
t_RP    	= r'\)'
t_VALI  	= r'\d+'
t_VALF  	= r'\d+\.\d+'
t_STR   	= r'\'.*\''
t_SEQ		= r'=='

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Error handling rule
def t_error(t):
        if(t.value[0] != None):
	    print "Illegal character ", t.value[0] ,
	    t.lexer.skip(1)

lex.lex()


