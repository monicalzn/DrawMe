import ply.lex as lex

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'program' : 'PR',
   'var' : 'V',
   'main' : 'MAIN',
   'int' : 'INT',
   'float' : 'FLOAT',
   'void' : 'VD',
   'global' : 'GL',
   'function': 'FUN',
   'penWidth':'PENW',
   'penPos':'PENP',
   'penColor':'PENC',
   'penX': 'PENX',
   'penY':'PENY',
   'setColor':'SETC',
   'backgroundColor' : 'BACO',
   'line':'LI',
   'rectangle' :'REC',
   'fill' :'FILL',
   'triangle' :'TRI',
   'circle' : 'CIR',
   'square' : 'SQ',
   'polygon' : 'POL',
   'angle' : 'A',
   'arc' : 'ARC',
   'lineStrip' : 'LS',
   'repeat' : 'RE',
   'return' : 'RT',
   'label' : 'LA',
}

#List of token name.
tokens = [
	'LB', 'RB', 'C', 'LP', 'RP', 'EQ', 'VALI', 'VALF', 'SEQ', 'D', 'MT', 'LT', 'ADD', 'SUB', 'M', 'DIV', 'STR', 'SC', 'ID', 'LC', 'RC'
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
t_C     	= r'\,'
t_LB    	= r'\{'
t_RB    	= r'\}'
t_LP    	= r'\('
t_RP    	= r'\)'
t_LC      = r'\['
t_RC      = r'\]'
t_VALI  	= r'\d+'
t_VALF  	= r'\d+\.\d+'
t_STR		= r'\'.*\''
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


