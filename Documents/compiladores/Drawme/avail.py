from stack import Stack
import sys

	
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
		self.scopeF = Stack()
		self.scope = ''
		self.RT = ''
		self.semantic_cube = {
		'=': {
			'int': {
				'int': 'int',
				'float': 'float'
			},
			'float': {
				'int': 'error',
				'float': 'float'
			}
		},
		'>': {
			'int': {
				'int': 'bool',
				'float': 'bool'
			},
			'float': {
				'int': 'bool',
				'float': 'bool'
			}
		},
		'<': {
			'int': {
				'int': 'bool',
				'float': 'bool'
			},
			'float': {
				'int': 'bool',
				'float': 'bool'
			}
		},
		'>=': {
			'int': {
				'int': 'bool',
				'float': 'bool'
			},
			'float': {
				'int': 'bool',
				'float': 'bool'
			}
		},
		'<=': {
			'int': {
				'int': 'bool',
				'float': 'bool'
			},
			'float': {
				'int': 'bool',
				'float': 'bool'
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
		#depending on the result from the semantic cube a new temporal will be created
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

	def get_type(self, operator, type1, type2): 
#operando1, operando2, operador, returns the corresponding type from the operation
		typ = self.semantic_cube.get(operator)
		if typ != None:
			typ = typ.get(type1)
			if typ != None:
				typ = typ.get(type2)
				return typ
		print 'error'	

	def setblock(self, block):
	#re-sets the memory for the next block
		self.block = block
		self.temp_int = 5000
		self.temp_float = 6000
		self.temp_bool = 4000 
		self.temp_dir = 7000 

	def getblock(self):
	#returns the current block
		return self.block
	
	def get_temp_dirs(self):
	#returns the memory needed for the temporals
		return [(self.temp_bool-4000), (self.temp_int-5000), (self.temp_float-6000), (self.temp_dir-7000)]

	def expression(self):
	#if there is an expression that needs to be resolved
		if(self.OpStack.size() > 0):
			if(self.OpStack.peek() == '>' or self.OpStack.peek() == '<' or self.OpStack.peek() == '<>' or self.OpStack.peek() == '==' or self.OpStack.peek() == '<=' or self.OpStack.peek() == '>='):
				self.quad()

	def add_sub(self):
	#if there is an operation that needs to be solved.
		if(self.OpStack.size() > 0):
			if(self.OpStack.peek() == '+' or self.OpStack.peek() == '-'):
				self.quad()

	def mul_div(self):
	#if there is an operation that needs to be solved.
		if(self.OpStack.size() > 0):
			if(self.OpStack.peek() == '*' or self.OpStack.peek() == '/'):
				self.quad()

	def rep_jump(self, dirOne, dirZero):
	#it substracts one to the value of the temporal previously created with the value of the repetition, checks if it's equal to zero, if it's not it will do the block again, so a gotof is crated.
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
	#creates an assign
		if(self.OStack.size() > 0):
			self.numQuad += 1
			spCuad = [101, self.OStack.pop(), -1, var]
			self.quads.append(spCuad)
			#meter temporal

	def condition_start(self):
	#at the end of the condition it fills the last goto that was created with the value of the current quad.
		if(self.jumps.size() > 0):
			jump = self.jumps.pop() - 1
			spCuad = self.quads[jump]
			spCuad[3] = self.numQuad 
			self.quads[jump] = spCuad

	def condition(self):
	#the start of the condition, creates a gotof and stores it, also stores the numQuad on the jump stack.
		condition = self.OStack.pop()
		cond_type = self.TStack.pop()
		if(cond_type != "bool"):
			print "error, type missmatch"
			sys.error(0)
		else:
			spCuad = ['GOTOF', condition, -1, -1]
			self.quads.append(spCuad)
			self.numQuad += 1
			self.jumps.push(self.numQuad)

	def condition_else(self):
	#if there is an else the goto from the if must be filled and a new goto must be created.
		jump = self.jumps.pop() -1
		spCuad = self.quads[jump]
		spCuad[3] = self.numQuad +1
		self.quads[jump] = spCuad
		spCuad = ['GOTO', -1, -1, -1]
		self.quads.append(spCuad)
		self.numQuad += 1
		self.jumps.push(self.numQuad)
	
	def main(self):
	#creates the goto of the main, stores the numQuad on the jump stack.
		spCuad = ['GOTO', -1, -1, -1]
		self.quads.append(spCuad)
		self.jumps.push(self.numQuad)
		self.numQuad += 1

	def main_goto(self):
	#fills the goto of the main.
		jump = self.jumps.pop()
		spCuad = self.quads[jump]
		spCuad[3] = self.numQuad 
		self.quads[jump] = spCuad
		
	def rep(self):
	#makes a copy of the number that represents the amount of times the block will be made, and store the value to the stack.
		h = self.get_temp('-', self.TStack.peek(), self.TStack.pop()) 
		tem = h[0]
		spCuad = [101, self.OStack.pop(), -1, tem]
		self.numQuad += 1
		self.quads.append(spCuad)
		self.jumps.push(self.numQuad)
		self.OStack.push(tem)
		self.TStack.push(h[1])

	def dim(self, dim, pointer):
	#for arrays, creates the quad that will verify the value is within range, creates a pointer where the direction of the value that we want will be stored. stores the temopral.
		spCuad = ['DIM', dim, pointer, -1]
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
	#for matrix, pointer represents row, multiply by two to get the "real value", check is not out of bounds, get pointer dir, create quad that will generate actual direction, add one to the pointer to get the next value for which you need a new prointer dir and a quad that will generat actual direction.
		h = self.get_temp('+', 'int', 'int') 
		tem = h[0]
		spCuad = ['*', pointer, '40002', tem]
		self.quads.append(spCuad)
		pointer = tem

		spCuad = ['DIM', dim, pointer, -1]
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
	#when initializing a matrix, check dimension, create the pointer for the assign do the assign samething with the next value. 
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
	#check dimentio, within bounds, get pointer dir, quad that will generate actual direction.
		spCuad = ['DIMC', dim, row, -1]
		self.quads.append(spCuad)
		
		h = self.get_temp('$', 'dir', -1) 
		tem = h[0]
		spCuad = ['DIRC', direction, row, tem]
		self.quads.append(spCuad)
		self.assig(tem)

		self.numQuad += 2

	def function_return(self, empty, vDir):
	#check if function has return, if it does creates proper quad.
		if(empty):
			spCuad = ['RETURN',-1, -1, -1]
			self.numQuad += 1
			self.quads.append(spCuad)
			return False
		else:
			spCuad = ['RETURN', self.OStack.pop(), -1, vDir]
			#self.OStack.push(vDir)
			self.numQuad += 1
			self.quads.append(spCuad)
			return True

	def function_end(self):
	#end of procedure quad.
		spCuad = ['ENDPROC', 1, -1, 1]
		self.numQuad += 1
		self.quads.append(spCuad)

	def function_param(self, param):
	#function parameters, check there are enough parameters, has to check the order of the parameters for correct assign.
		cont = len(param)
		if self.OStack.size() < cont:
			print "Missing parameters."
			sys.exit(0)
		listh = []
		cont = len(param) -1		
		while cont >= 0:
			for key in param:
				if cont == param[key][1]:
					spCuad = ['PARAMETRO', self.OStack.pop(), -1, param[key][2]]
					print spCuad
					cont -= 1
					self.numQuad += 1
					self.quads.append(spCuad)

	def call_function(self, var):
	#quad that will store the name of the function for which memory is needed
		spCuad = ['ERA', -1, -1, var]
		self.numQuad += 1
		self.quads.append(spCuad)
		self.OpStack.push('(')

	def call_function_end(self,var, vDir, temp):
	#go sub that has the name of the function to which we will go, create an assign in case there is a returning value to a new temporal.
		spCuad = ['GOSUB', -1, -1, var]
		self.numQuad += 1
		self.quads.append(spCuad)
		spCuad = ['101', vDir, -1, temp]
		self.OStack.push(temp)
		self.numQuad += 1
		self.quads.append(spCuad)
		self.OpStack.pop()
		
	def append_quad(self, quad):
	#appends quad
		self.numQuad += 1
		self.quads.append(quad)

	def append_quad_one(self, fun):
	#used by functions that only have one parameter.
		self.numQuad += 1
		spQuad = [fun, self.OStack.pop(), -1, -1]
		self.TStack.pop()
		self.quads.append(spQuad)

	def append_quad_two(self, fun):
	#used by functions that have two parameters.
		self.numQuad += 1
		two = self.OStack.pop()
		self.TStack.pop()
		spQuad = [fun, self.OStack.pop(),two, -1]
		self.TStack.pop()
		self.quads.append(spQuad)

	def append_quad_three(self, fun):
	#used by functions that have three parameters.
		self.numQuad += 1
		blue = self.OStack.pop()
		self.TStack.pop()
		green = self.OStack.pop()
		self.TStack.pop()
		spQuad = [fun, self.OStack.pop(), green, blue]
		self.TStack.pop()
		self.quads.append(spQuad)

	def append_quad_tri(self, fun):
	#used by triangle to create the necessary quads with the information in the right order.
		self.numQuad += 2
		y3 = self.OStack.pop()
		self.TStack.pop()
		x3 = self.OStack.pop()
		self.TStack.pop()
		y2 = self.OStack.pop()
		self.TStack.pop()
		x2 = self.OStack.pop()
		self.TStack.pop()
		y = self.OStack.pop()
		self.TStack.pop()
		x = self.OStack.pop()
		self.TStack.pop()
		spQuad = [fun, x, y, -1]
		self.quads.append(spQuad)
		spQuad = [x2, y2, x3, y3]
		self.quads.append(spQuad)

	def quad(self):
	#used by expressions to create quads.
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
	#prints information.
		print self.OStack.printi()

	def get_temp_point(self):
	#create a pointer direction
		h = self.get_temp('$', 'dir', -1)
		return h[0]
		

	def OpStack_pop(self):
		self.OpStack.pop()

	def OpStack_push(self, op):
		self.OpStack.push(op)

	def TStack_push(self, op):
		self.TStack.push(op)

	def TStack_pop(self, ):
		self.TStack.pop()

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

	def setFuncScope(self, scope):
		self.scopeF.push(scope)

	def delFuncScope(self):
		self.scopeF.pop()

	def getFuncScope(self):
		return self.scopeF.peek()
	
	def setRT(self, RT):
		self.RT = RT

	def getRT(self):
		return self.RT

	def setfuncQuad(self):
		self.funcQuad = self.numQuad

	def getfuncQuad(self):
		return self.funcQuad
