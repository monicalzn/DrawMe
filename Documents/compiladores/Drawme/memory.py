
class Memory:

	def __init__(self):
		int_size = float_size = bool_size = 0
		self.int_block = None
		self.float_block = None
		self.temp_bool_block = None
		self.temp_int_block = None
		self.temp_float_block = None

	def setMem(self, intQ, floatQ, boolQ, intTQ, floatTQ):
		self.int_block = [0] * intQ
		self.float_block = [0.0] * floatQ
		self.temp_bool_block = [True] * boolQ
		self.temp_int_block = [0] * intTQ
		self.temp_float_block = [0.0] * floatTQ

	def writeValue(self, vDir, value):
		print "WRITEV ", vDir, "  ",value 
		if(vDir >= 2000 and vDir <= 2999):
			self.int_block[(vDir-2000)] = int(value)
		elif(vDir >= 3000 and vDir <= 3999):
			self.float_block[(vDir-3000)] = float(value)
		elif(vDir >= 4000 and vDir <= 4999):
			self.temp_bool_block[(vDir-4000)] = bool(value)
		elif(vDir >= 5000 and vDir <= 5999):
			self.temp_int_block[(vDir-5000)] = int(value)
		elif vDir >= 6000 and vDir >= 5999:
			self.temp_float_block[(vDir-6000)] = float(value)

	def readValue(self, vDir):
		if(vDir >= 2000 and vDir <= 2999):
			return self.int_block[(vDir-2000)]
		elif(vDir >= 3000 and vDir <= 3999):
			return self.float_block[(vDir-3000)]
		elif(vDir >= 4000 and vDir <= 4999):
			return self.temp_bool_block[(vDir-4000)]
		elif(vDir >= 5000 and vDir <= 5999):
			return self.temp_int_block[(vDir-5000)]
		elif vDir >= 6000 and vDir >= 5999:
			return self.temp_float_block[(vDir-6000)]
