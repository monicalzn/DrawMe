from stack import Stack


	
class avail:
	semantic_cube = None
	
	def __init__(self):
		self.next_temp = 1
		self.temp_used = Stack()
		self.temp_unused = Stack()
		self.OStack = Stack()  #Operand Stack
		self.TStack = Stack() #Type stack
		self.OpStack = Stack() #Operator stack
		self.jumps = Stack() #jump stack
		self.numQuad = 0
		self.funcQuad = 0
		self.temp_int = 5000
		self.temp_float = 6000
		self.temp_bool = 4000 
		self.temp_dir = 7000 
		self.quads = []
		self.DStack = Stack()
		self.IDStack = Stack()
		self.block = 0
		self.scope = ''
		self.RT = ''
		self.semantic_cube = {
		'=': {
			'int': {
				'int': 'int',
				'float': 'error'
			},
			'float': {
				'int': 'error',
				'float': 'float'
			}
		},
		'>': {
			'int': {
				'int': 'bool',
				'float': 'bool',
				'TEXTO': 'error'
			},
			'float': {
				'int': 'bool',
				'float': 'bool',
				'TEXTO': 'error'
			}
		},
		'<': {
			'int': {
				'int': 'bool',
				'float': 'bool',
				'TEXTO': 'error'
			},
			'float': {
				'int': 'bool',
				'float': 'bool',
				'TEXTO': 'error'
			},
			'TEXTO': {
				'int': 'error',
				'float': 'error',
				'TEXTO': 'bool'
			}
		},
		'<>': {
			'int': {
				'int': 'bool',
				'float': 'bool'
			},
			'float': {
				'int': 'bool',
				'float': 'bool'
			}
		},
		'==': {
			'int': {
				'int': 'bool',
				'float': 'bool'
			},
			'float': {
				'int': 'bool',
				'float': 'bool'
			}
		},
		'+': {
			'int': {
				'int': 'int',
				'float': 'float'
			},
			'float': {
				'int': 'float',
				'float': 'float'
			}
		},
		'-': {
			'int': {
				'int': 'int',
				'float': 'float'
			},
			'float': {
				'int': 'float',
				'float': 'float'
			}
		},
		'*': {
			'int': {
				'int': 'int',
				'float': 'float'
			},
			'float': {
				'int': 'float',
				'float': 'float'
			}
		},
		'/': {
			'int': {
				'int': 'int',
				'float': 'float'
			},
			'float': {
				'int': 'float',
				'float': 'float'
			}
		},
		'$': {
			'dir': {
				'-1': 'dir'
			}
		}
	}

	def get_temp(self, operator, type1, type2):
		temp_type = self.get_type(operator, type1, type2)
		if temp_type == 'int':
			temp = self.temp_int
			self.temp_int += 1 
		elif temp_type == 'float':
			temp = self.temp_float
			self.temp_float += 1
		elif temp_type == 'bool':
			temp = self.temp_bool
			self.temp_bool += 1
		elif type1 == 'dir':
			temp = self.temp_dir
			self.temp_dir += 1
		temp += (self.block * 10000)
		return [temp, self.get_type(operator, type1, type2)]

	def get_type(self, operator, type1, type2): #operando1, operando2, operador
		typ = self.semantic_cube.get(operator)
		if typ != None:
			typ = typ.get(type1)
			if typ != None:
				typ = typ.get(type2)
				return typ
		print 'error'	

	def setblock(self, block):
		self.block = block
		self.temp_int = 5000
		self.temp_float = 6000
		self.temp_bool = 4000 
		self.temp_dir = 7000 

	def getblock(self):
		return self.block
	
	def get_temp_dirs(self):
		return [(self.temp_bool-4000), (self.temp_int-5000), (self.temp_float-6000), (self.temp_dir-7000)]

	def expression(self):
		if(self.OpStack.size() > 0):
			if(self.OpStack.peek() == '>' or self.OpStack.peek() == '<' or self.OpStack.peek() == '<>' or self.OpStack.peek() == '=='):
				self.quad()

	def add_sub(self):
		if(self.OpStack.size() > 0):
			if(self.OpStack.peek() == '+' or self.OpStack.peek() == '-'):
				self.quad()

	def mul_div(self):
		if(self.OpStack.size() > 0):
			if(self.OpStack.peek() == '*' or self.OpStack.peek() == '/'):
				self.quad()

	def rep_jump(self, dirOne, dirZero):
		tem = self.OStack.pop()
		spCuad = ['-', tem, dirOne, tem]
		self.numQuad += 1
		self.quads.append(spCuad)
		jump = self.jumps.pop()
		h = self.get_temp('==', self.TStack.pop(), 'int') 
		spCuad = ['==', tem, dirZero, h[0]]
		self.numQuad += 1
		self.quads.append(spCuad)
	
		spCuad = ['GOTOF', h[0], -1, jump]
		self.numQuad += 1
		self.quads.append(spCuad)

	def assig(self, var):
		if(self.OStack.size() > 0):
			self.numQuad += 1
			spCuad = [101, self.OStack.pop(), -1, var]
			self.quads.append(spCuad)
			#meter temporal

	def condition_start(self):
		if(self.jumps.size() > 0):
			jump = self.jumps.pop() - 1
			spCuad = self.quads[jump]
			spCuad[3] = self.numQuad 
			self.quads[jump] = spCuad

	def condition(self):
		condition = self.OStack.pop()
		cond_type = self.TStack.pop()
		if(cond_type != "bool"):
			print "error, type missmatch"
		else:
			spCuad = ['GOTOF', condition, -1, -1]
			self.quads.append(spCuad)
			self.numQuad += 1
			self.jumps.push(self.numQuad)

	def condition_else(self):
		jump = self.jumps.pop() -1
		spCuad = self.quads[jump]
		spCuad[3] = self.numQuad +1
		self.quads[jump] = spCuad
		spCuad = ['GOTO', -1, -1, -1]
		self.quads.append(spCuad)
		self.numQuad += 1
		self.jumps.push(self.numQuad)
	
	def main(self):
		spCuad = ['GOTO', -1, -1, -1]
		self.quads.append(spCuad)
		self.jumps.push(self.numQuad)
		self.numQuad += 1

	def main_goto(self):
		jump = self.jumps.pop()
		spCuad = self.quads[jump]
		spCuad[3] = self.numQuad 
		self.quads[jump] = spCuad
		
	def rep(self):
		h = self.get_temp('-', self.TStack.peek(), self.TStack.pop()) 
		tem = h[0]
		spCuad = [101, self.OStack.pop(), -1, tem]
		self.numQuad += 1
		self.quads.append(spCuad)
		self.jumps.push(self.numQuad)
		self.OStack.push(tem)
		self.TStack.push(h[1])

	def dim(self, dim, pointer):
		spCuad = ['DIM', dim, pointer, -1]
		print "DIM", spCuad		
		self.numQuad += 1
		self.quads.append(spCuad)
		self.numQuad += 1
		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		spCuad = ['DIR', self.OStack.pop(), pointer, tem]
		self.quads.append(spCuad)	
		#meter temporal
		self.OStack.push(tem)
	
	def dimT(self, dim, pointer):
		h = self.get_temp('+', 'int', 'int') 
		tem = h[0]
		spCuad = ['*', pointer, '40002', tem]
		self.quads.append(spCuad)
		pointer = tem

		spCuad = ['DIM', dim, pointer, -1]
		print "DIM", dim
		self.quads.append(spCuad)
		
		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		ren = self.OStack.pop()
		spCuad = ['DIR', ren, pointer, tem]
		one = tem
		self.quads.append(spCuad)	
		#meter temporal
		h = self.get_temp('+', 'int', 'int') 
		tem = h[0]
		spCuad = ['+', pointer, '40000', tem]
		self.quads.append(spCuad)
		self.OStack.push(tem)
		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		spCuad = ['DIR', ren, self.OStack.pop(), tem]
		self.quads.append(spCuad)	
		#meter temporal
		help = self.OStack.pop()
		self.OStack.push(tem)
		self.OStack.push(help)
		self.OStack.push(one)
		self.numQuad += 4

	def dimTP(self, direction, row, dim):
		row *= 2
		spCuad = ['DIMC', dim, row, -1]
		self.quads.append(spCuad)
		
		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		spCuad = ['DIRC', direction, (row+1), tem]
		self.quads.append(spCuad)
		self.assig(tem)

		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		spCuad = ['DIRC', direction, row, tem]
		self.quads.append(spCuad)
		self.assig(tem)

		self.numQuad += 3

	def dimP(self, direction, row, dim):
		spCuad = ['DIMC', dim, row, -1]
		self.quads.append(spCuad)
		
		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		spCuad = ['DIRC', direction, row, tem]
		self.quads.append(spCuad)
		self.assig(tem)

		self.numQuad += 2

	def function_return(self, empty, vDir):
		if(empty):
			spCuad = ['RETURN',-1, -1, -1]
			self.numQuad += 1
			self.quads.append(spCuad)
		else:
			spCuad = ['RETURN', self.OStack.pop(), -1, vDir]
			self.OStack.push(vDir)
			self.numQuad += 1
			self.quads.append(spCuad)

	def function_end(self):
		spCuad = ['RET', -1, -1, -1]
		self.numQuad += 1
		self.quads.append(spCuad)
		spCuad = ['ENDPROC', 1, -1, 1]
		self.numQuad += 1
		self.quads.append(spCuad)

	def function_param(self, param):
		listh = []
		cont = len(param)-1
		for key in param:
			listh.append(self.OStack.pop())
		for key in param:
			spCuad = ['PARAMETRO', listh[cont], -1, param[key][2]]
			cont -= 1
			self.numQuad += 1
			self.quads.append(spCuad)

	def call_function(self, var):
		spCuad = ['ERA', -1, -1, var]
		self.numQuad += 1
		self.quads.append(spCuad)

	def call_function_end(self,var):
		spCuad = ['GOSUB', -1, -1, var]
		self.numQuad += 1
		self.quads.append(spCuad)
		
	def append_quad(self, quad):
		self.numQuad += 1
		self.quads.append(quad)

	def append_quad_one(self, fun):
		self.numQuad += 1
		spQuad = [fun, self.OStack.pop(), -1, -1]
		self.quads.append(spQuad)

	def append_quad_two(self, fun):
		self.numQuad += 1
		two = self.OStack.pop()
		spQuad = [fun, self.OStack.pop(),two, -1]
		self.quads.append(spQuad)

	def append_quad_three(self, fun):
		self.numQuad += 1
		blue = self.OStack.pop()
		green = self.OStack.pop()
		spQuad = [fun, self.OStack.pop(), green, blue]
		self.quads.append(spQuad)

	def append_quad_tri(self, fun):
		self.numQuad += 2
		y3 = self.OStack.pop()
		x3 = self.OStack.pop()
		y2 = self.OStack.pop()
		x2 = self.OStack.pop()
		y = self.OStack.pop()
		x = self.OStack.pop()
		spQuad = [fun, x, y, -1]
		self.quads.append(spQuad)
		spQuad = [x2, y2, x3, y3]
		self.quads.append(spQuad)

	def quad(self):
		self.numQuad += 1
		h = self.get_temp(self.OpStack.peek(), self.TStack.pop(), self.TStack.pop()) 
		tem = h[0]
		second = self.OStack.pop() 
		spCuad = [self.OpStack.pop(), self.OStack.pop(), second, tem]
		self.quads.append(spCuad)	
		#meter temporal
		self.OStack.push(tem)
		self.TStack.push(h[1])

	def printS(self):
		print self.OStack.printi()

	def OpStack_pop(self):
		self.OpStack.pop()

	def OpStack_push(self, op):
		self.OpStack.push(op)

	def TStack_push(self, op):
		self.TStack.push(op)

	def OStack_push(self, op):
		self.OStack.push(op)
		
	def OStack_pop(self):
		return self.OStack.pop()

	def OStack_peek(self):
		return self.OStack.peek()
	
	def DStack_push(self, op):
		self.DStack.push(op)
		
	def DStack_pop(self):
		return self.DStack.pop()

	def IDStack_push(self, op):
		self.IDStack.push(op)
		
	def IDStack_pop(self):
		return self.IDStack.pop()

	def print_quads(self):
		print self.quads

	def get_quads(self):
		return self.quads

	def setScope(self, scope):
		self.scope = scope

	def getScope(self):
		return self.scope
	
	def setRT(self, RT):
		self.RT = RT

	def getRT(self):
		return self.RT

	def setfuncQuad(self):
		self.funcQuad = self.numQuad

	def getfuncQuad(self):
		return self.funcQuad
