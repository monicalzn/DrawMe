
class memory:

	def __init__(self):
		int_size = float_size = bool_size = 0
		self.int_block = None
		self.float_block = None
		self.temp_bool_block = None
		self.temp_int_block = None
		self.temp_float_block = None

	def setMem(self, intQ, floatQ, boolQ):
		self.int_block = []
		self.float_block = []
		self.temp_bool_block = []
		self.temp_int_block = []
		self.temp_float_block = []

	def writeValue(self, vDir, value):
		if(vDir >= 2000 and vDir <= 2999):
			self.int_block[(vDir-2000)] = value
		else if(vDir >= 3000 and vDir <= 3999):
			self.float_block[(vDir-3000)] = value
		else if(vDir >= 4000 and vDir <= 4999):
			self.temp_bool_block[(vDir-4000)] = value
		else if(vDir >= 5000 and vDir <= 5999):
			self.temp_int_block[(vDir-5000)] = value
		else if vDir >= 6000 and vDir >= 5999:
			self.temp_float_block[(vDir-6000)] = value

	def readValue(self, vDir):
		if(vDir >= 2000 and vDir <= 2999):
			return self.int_block[(vDir-2000)]
		else if(vDir >= 3000 and vDir <= 3999):
			return self.float_block[(vDir-3000)]
		else if(vDir >= 4000 and vDir <= 4999):
			return self.temp_bool_block[(vDir-4000)]
		else if(vDir >= 5000 and vDir <= 5999):
			return self.temp_int_block[(vDir-5000)]
		else if vDir >= 6000 and vDir >= 5999:
			return self.temp_float_block[(vDir-6000)]
