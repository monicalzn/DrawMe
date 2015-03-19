class cuboSemantico:
	cubo_semantico = None

	def __init__(self):
		self.cubo_semantico = {
		'=': {
			'ENTERO': {
				'ENTERO': 'ENTERO',
				'DECIMAL': None,
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': None,
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'TEXTO'
			}
		},
		'&&': {
			'ENTERO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': None
			},
			'DECIMAL': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': None
			},
			'bool': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': 'bool'
			}
		},
		'||': {
			'ENTERO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': None
			},
			'DECIMAL': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': None
			},
			'bool': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None,
				'bool': 'bool'
			}
		},
		'>': {
			'ENTERO': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'bool'
			}
		},
		'<': {
			'ENTERO': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'bool'
			}
		},
		'!=': {
			'ENTERO': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'bool'
			}
		},
		'>=': {
			'ENTERO': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'bool'
			}
		},
		'<=': {
			'ENTERO': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'bool'
			}
		},
		'==': {
			'ENTERO': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'bool',
				'DECIMAL': 'bool',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': 'bool'
			}
		},
		'+': {
			'ENTERO': {
				'ENTERO': 'ENTERO',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'DECIMAL',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None
			}
		},
		'-': {
			'ENTERO': {
				'ENTERO': 'ENTERO',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'DECIMAL',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None
			}
		},
		'*': {
			'ENTERO': {
				'ENTERO': 'ENTERO',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'DECIMAL',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None
			}
		},
		'/': {
			'ENTERO': {
				'ENTERO': 'ENTERO',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'DECIMAL': {
				'ENTERO': 'DECIMAL',
				'DECIMAL': 'DECIMAL',
				'TEXTO': None
			},
			'TEXTO': {
				'ENTERO': None,
				'DECIMAL': None,
				'TEXTO': None
			}
		}
	}

	def checarSemanticaExp(self,oper1,oper2,op):
		res = self.cubo_semantico.get(op)
		if res != None:
			res = res.get(oper1)
			if res != None:
				res = res.get(oper2)
		return res
