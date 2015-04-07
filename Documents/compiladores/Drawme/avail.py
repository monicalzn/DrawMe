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
		self.quads = []
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
		}
	}

	def get_temp(self, operator, type1, type2):
		if(self.temp_unused.size() == 0):
			temp = 't' + str(self.next_temp)
			self.temp_used.push(temp)
			self.next_temp += 1
		else:
			temp = self.temp_unused.pop()
		return [temp, self.get_type(operator, type1, type2)]

	def get_type(self, operator, type1, type2): #operando1, operando2, operador
		typ = self.semantic_cube.get(operator)
		if typ != None:
			typ = typ.get(type1)
			if typ != None:
				typ = typ.get(type2)
				return typ
		print 'error'	

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

	def rep_jump(self):
		tem = self.OStack.pop()
		spCuad = ['-', tem, 1, tem]
		self.numQuad += 1
		self.quads.append(spCuad)
		self.jumps.push(numQuad)
		jump = self.jumps.pop()
		print "JJ", jump
		h = self.get_temp('==', self.TStack.pop(), 'int') 
		spCuad = ['==', tem, 0, h[0]]
		numQuad += 1
		self.quads.append(spCuad)
	
		spCuad = ['GOTOT', h[0], -1, jump]
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
			spCuad[3] = self.numQuad + 1
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
			self.jumps.push(numQuad)

	def condition_else(self):
		jump = self.jumps.pop() -1
		spCuad = self.quads[jump]
		spCuad[3] = numQuad +2
		self.quads[jump] = spCuad
		spCuad = ['GOTO', -1, -1, -1]
		self.quads.append(spCuad)
		self.numQuad += 1
		self.jumps.push(numQuad)

	def rep(self):
		h = self.get_temp('-', self.TStack.peek(), self.TStack.pop()) 
		tem = h[0]
		spCuad = ['=', self.OStack.pop(), -1, tem]
		self.numQuad += 1
		self.quads.append(spCuad)
	
		self.OStack.push(tem)
		self.TStack.push(h[1])

	def append_quad(self, quad):
		self.numQuad += 1
		self.quads.append(quad)

	def append_quad_one(self, fun):
		self.numQuad += 1
		spQuad = [fun, self.OStack.pop(), -1, -1]
		self.quads.append(spQuad)

	def append_quad_two(self, fun):
		self.numQuad += 1
		spQuad = [fun, self.OStack.pop(), self.OStack.pop(), -1]
		self.quads.append(spQuad)

	def append_quad_three(self, fun):
		self.numQuad += 1
		spQuad = [fun, self.OStack.pop(), self.OStack.pop(), self.OStack.pop()]
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


	def OpStack_pop(self):
		self.OpStack.pop()

	def OpStack_push(self, op):
		self.OpStack.push(op)

	def TStack_push(self, op):
		self.TStack.push(op)

	def OStack_push(self, op):
		self.OStack.push(op)
		
	def print_quads(self):
		print self.quads

	def get_quads(self):
		return self.quads