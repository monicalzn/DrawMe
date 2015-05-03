from memory import Memory

class MemoryAdministrator:

	def __init__(self):
		self.constants_int = []
		self.constants_float = []
		self.constants_str = []
		self.pointers = []
		self.globals = Memory()
		self.main = Memory()
		self.currentScope = 0
		self.functions = dict()

	def constSize(self, sizeI, sizeF, sizeS):
		self.constants_int = [0] * sizeI
		self.constants_float = [0.0] * sizeF
		self.constants_str = [0] * sizeS
	
	def setMainMem(self, strQ, intQ, floatQ, boolQ, intTQ, floatTQ, pointQ):
		self.main.setMem(int(strQ), int(intQ), int(floatQ), int(boolQ), int(intTQ), int(floatTQ), int(pointQ))

	def setGlobalMem(self, strQ, intQ, floatQ, boolQ, intTQ, floatTQ, pointQ):
		self.globals.setMem(int(strQ), int(intQ), int(floatQ), int(boolQ), int(intTQ), int(floatTQ), int(pointQ))

	def setFunction(self, strQ, intQ, floatQ, boolQ, intTQ, floatTQ, pointQ):
		function = Memory()
		function.setMem(int(strQ), int(intQ), int(floatQ), int(boolQ), int(intTQ), int(floatTQ), int(pointQ))
		
		self.functions[self.currentScope+1] = function
		print "FUNCTION ", self.currentScope

	def changeScope(self):
		self.currentScope += 1

	def delete_function(self):
		self.functions[self.currentScope].releseMem()
		del self.functions[self.currentScope]
		self.currentScope -= 1

	def writeValue(self, dirV, value):
		if dirV[1] == '7':
			dirV = int(dirV)			
			if((dirV-10000) < 10000):
				#global values
				dirV = self.globals.readValue(dirV-10000)
			elif((dirV-20000) < 10000):
				#main values
				print "MAIN&7 ", self.main.readValue(dirV-20000)
				dirV = self.main.readValue(dirV-20000)
			elif((dirV-30000) < 10000):
				#function values
				dirV = self.functions[self.currentScope].readValue(dirV-30000)
			dirV = str(dirV)
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
		if((dirV-30000) < 10000):
			#function values
			dirV = dirV-30000
			self.functions[self.currentScope].writeValue(dirV, value)
			return
		if((dirV - 40000) < 10000):
			#constants
			dirV = dirV-40000
			if(dirV < 1000):
				self.constants_int[dirV] = int(value)
			elif(dirV < 2000):
				self.constants_float[dirV-1000] = float(value)
			else:
				self.constants_str[dirV-2000] = str(value)
			return

	def writeValueS(self, dirV, value):
		#diferente function for writting values it's only used with PARAM due to the fact that it's sending information to a diferent scope
		if dirV[1] == '7':
			dirV = int(dirV)			
			if((dirV-10000) < 10000):
				#global values
				dirV = self.globals.readValue(dirV-10000)
			elif((dirV-20000) < 10000):
				#main values
				print "MAIN&7 ", self.main.readValue(dirV-20000)
				dirV = self.main.readValue(dirV-20000)
			elif((dirV-30000) < 10000):
				#function values
				dirV = self.functions[self.currentScope+1].readValue(dirV-30000)
			dirV = str(dirV)
		dirV = int(dirV)	
		#print "DIRECTION ", dirV		
		if((dirV-10000) < 10000):
			#global values
			dirV = dirV-10000
			self.globals.writeValue(dirV, value)
			return
		if((dirV - 20000) < 10000):
			#main values
			dirV = dirV-20000
			self.main.writeValue(dirV, value)
			return
		if((dirV-30000) < 10000):
			#function values
			dirV = dirV-30000
			self.functions[self.currentScope+1].writeValue(dirV, value)
			return

	def getValue(self, dirV):
		if dirV[1] == '7':
		#if the direction is a pointer you have to retrieve the actual direction
			dirV = int(dirV)			
			if((dirV-10000) < 10000):
				#global values
				dirV = self.globals.readValue(dirV-10000)
			elif((dirV-20000) < 10000):
				#main values
				print "MAIN&7 ", self.main.readValue(dirV-20000)
				dirV = self.main.readValue(dirV-20000)
			elif((dirV-30000) < 10000):
				#function values
				dirV = self.functions[self.currentScope].readValue(dirV-30000)
			dirV = str(dirV)
		
		dirV = int(dirV)		
		if((dirV-10000) < 10000):
			#global values
			dirV = dirV-10000
			return self.globals.readValue(dirV)
		if((dirV-20000) < 10000):
			#main values
			dirV = dirV-20000
			return self.main.readValue(dirV)
		if((dirV-30000) < 10000):
			#function values
			dirV = dirV-30000
			return self.functions[self.currentScope].readValue(dirV)
		if((dirV - 40000) < 10000):
			#constants
			dirV = dirV-40000
			if(dirV < 1000):
				return int(self.constants_int[dirV])
			elif(dirV < 2000):
				return float(self.constants_float[dirV-1000])
			else:
				return str(self.constants_str[dirV-2000])


	def writePointValue(self, dirV, value):
		dirV = int(dirV)		
		if((dirV-10000) < 10000):
			#global values
			dirV = dirV-10000
			self.globals.writeValue(dirV, value)
			return
		if((dirV - 20000) < 10000):
			#main values
			dirV = dirV-20000
			self.main.writeValue(dirV, value)
			return
		if((dirV-30000) < 10000):
			#function values
			dirV = dirV-30000
			self.functions[self.currentScope].writeValue(dirV, value)
			return

	def printFunctions(self):
		print self.currentScope

	def printMain(self):
		self.main.printstuff()
	
	def printGl(self):
		self.globals.printstuff()

	def constPrint(self):
		print self.constants_int, " ", self.constants_float
