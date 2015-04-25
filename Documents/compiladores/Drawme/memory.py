
class Memory:

	def __init__(self):
		self.int_block = []
		self.float_block = []
		self.temp_bool_block = []
		self.temp_int_block = []
		self.temp_float_block = []
		self.pointers = []

	def setMem(self, intQ, floatQ, boolQ, intTQ, floatTQ, pointQ):
		self.int_block = [0] * intQ
		self.float_block = [0.0] * floatQ
		self.temp_bool_block = [True] * boolQ
		self.temp_int_block = [0] * intTQ
		self.temp_float_block = [0.0] * floatTQ
		self.pointers = [0] * pointQ
	
	def printstuff(self):
		print "int", self.int_block, "float", self.float_block, "Tbool", self.temp_bool_block, "Tint", self.temp_int_block, "Tfloat", self.temp_float_block

	def writeValue(self, vDir, value):
		if(vDir >= 2000 and vDir <= 2999):
			self.int_block[(vDir-2000)] = int(value)
		elif(vDir >= 3000 and vDir <= 3999):
			self.float_block[(vDir-3000)] = float(value)
		elif(vDir >= 4000 and vDir <= 4999):
			self.temp_bool_block[(vDir-4000)] = bool(value)
		elif(vDir >= 5000 and vDir <= 5999):
			self.temp_int_block[(vDir-5000)] = int(value)
		elif vDir >= 6000 and vDir <= 6999:
			self.temp_float_block[(vDir-6000)] = float(value)
		elif(vDir >= 7000 and vDir <= 7999):
			self.pointers[(vDir-7000)] = int(value)

	def readValue(self, vDir):
		if(vDir >= 2000 and vDir <= 2999):
			return self.int_block[(vDir-2000)]
		elif(vDir >= 3000 and vDir <= 3999):
			return self.float_block[(vDir-3000)]
		elif(vDir >= 4000 and vDir <= 4999):
			return self.temp_bool_block[(vDir-4000)]
		elif vDir >= 5000 and vDir <= 5999:
			return self.temp_int_block[(vDir-5000)]
		elif vDir >= 6000 and vDir <= 6999:
			return self.temp_float_block[(vDir-6000)]
		elif vDir >= 7000 and vDir <= 7999:
			return self.pointers[(vDir-7000)]

	def releseMem(self):
		del self.int_block
		del self.float_block
		del self.temp_bool_block
		del self.temp_int_block 
		del self.temp_float_block 
		del self.pointers
