from memory import Memory

class MemoryAdministrator:

	def __init__(self):
		self.constants_int = []
		self.constants_float = []
		self.globals = Memory()
		self.main = Memory()
	
	def constSize(self, sizeI, sizeF):
		self.constants_int = [0] * sizeI
		self.constants_float = [0.0] * sizeF
	
	def setMainMem(self, intQ, floatQ, boolQ, intTQ, floatTQ):
		self.main.setMem(int(intQ), int(floatQ), int(boolQ), int(intTQ), int(floatTQ))

	def setGlobalMem(self, intQ, floatQ, boolQ, intTQ, floatTQ):
		self.globals.setMem(int(intQ), int(floatQ), int(boolQ), int(intTQ), int(floatTQ))

	def writeValue(self, dirV, value):
		dirV = int(dirV)	
		#print "DIRECTION ", dirV		
		if((dirV-10000) < 10000):
			#global values
			#print "ADMINGLOBAL ", dirV
			dirV = dirV-10000
			self.globals.writeValue(dirV, value)
			return
		if((dirV - 20000) < 10000):
			#main values
			dirV = dirV-20000
			self.main.writeValue(dirV, value)
			return
		#if((30000 - dirV) < 10000):
			#function values
		if((dirV - 40000) < 10000):
			#constants
			dirV = dirV-40000
			if(dirV < 1000):
				self.constants_int[dirV] = int(value)
			else:
				#print dirV
				self.constants_float[dirV-1000] = float(value)
			return

	def getValue(self, dirV):
		dirV = int(dirV)			
		if((dirV-10000) < 10000):
			#global values
			dirV = dirV-10000
			return self.globals.readValue(dirV)
		if((dirV-20000) < 10000):
			#main values
			dirV = dirV-20000
			return self.main.readValue(dirV)
		#if((30000 - dirV) < 10000):
			#function values
		if((dirV - 40000) < 10000):
			#constants
			dirV = dirV-40000
			if(dirV < 1000):
				return int(self.constants_int[dirV])
			else:
				return float(self.constants_float[dirV-1000])

	def printMain(self):
		self.main.printstuff()
	
	def printGl(self):
		self.globals.printstuff()

	def constPrint(self):
		print self.constants_int, " ", self.constants_float
