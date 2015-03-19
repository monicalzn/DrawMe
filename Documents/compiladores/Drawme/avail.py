from stack import Stack


	
class avail:
	semantic_cube = None
	
	

	def __init__(self):
		self.next_temp = 1
		self.temp_used = Stack()
		self.temp_unused = Stack()
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
			},
			'TEXTO': {
				'int': 'error',
				'float': 'error',
				'TEXTO': 'bool'
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
		print self.next_temp
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
	
