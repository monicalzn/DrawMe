import sys
import math
from Tkinter import *
from MemoryAdministrator import MemoryAdministrator
from stack import Stack

actionPointer = Stack()
memory = MemoryAdministrator()
quads = []
proc = dict()
run = True
current_quad = 0
fill = False
penColor = '#000000000'
fillColor = '#000000000'
penWidth = 1

def actions():
	while(run):
		print "QUADS", quads[current_quad], " ", memory.getValue('40000')
		options[quads[current_quad][0]]()

def add():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	print "ADD ", quads[current_quad][1], " + ", second, " IN ", quads[current_quad][3]  
	result = first + second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def substract():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	print "SUB ", first, " - ", second, " IN ", quads[current_quad][3]  
	result = first - second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def multiply():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " * ", second, " IN ", quads[current_quad][3]  
	result = first * second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def divide():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " / ", second, " = ", first/second, " IN ", quads[current_quad][3]  
	result = first / second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def less_than():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	print "LESSSS ", first, " / ", second, " = ", first<second, " IN ", quads[current_quad][3]  
	result = first < second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def more_than():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	print "MOREE ", first, " / ", second, " = ", first>second, " IN ", quads[current_quad][3]  
	result = first > second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def different_than():
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " / ", second, " = ", first/second, " IN ", quads[current_quad][3]  
	result = first != second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def equal_to():
	global current_quad
	print "EQUAL ", quads[current_quad]
	memory.printFunctions()
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	print "Equal ", first, " / ", second, " =  IN ", quads[current_quad][3]  
	result = first == second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def setColor():
	global current_quad
	current_quad += 1

def stringColor(red, green, blue):
	if(red > 255):
		red = 255
	if(green > 255):
		green = 255
	if(blue > 255):
		blue = 255
	
	color = '#' + str(format(red, '02x')) + str(format(green, '02x')) + str(format(blue, '02x'))
	return color

def pencolor():
	global current_quad, penColor
	red = memory.getValue(quads[current_quad][1])
	green = memory.getValue(quads[current_quad][2])
	blue = memory.getValue(quads[current_quad][3])
	
	penColor = stringColor(red, green, blue)
	print "PENCOLOR", penColor
	current_quad += 1

def color():
	global current_quad, fillColor
	red = memory.getValue(quads[current_quad][1])
	green = memory.getValue(quads[current_quad][2])
	blue = memory.getValue(quads[current_quad][3])
	
	fillColor = stringColor(red, green, blue)
	print "PENCOLOR", fillColor
	current_quad += 1
	
def backColor():
	global current_quad, penWidth
	red = memory.getValue(quads[current_quad][1])
	green = memory.getValue(quads[current_quad][2])
	blue = memory.getValue(quads[current_quad][3])
	
	color = stringColor(red, green, blue)
	w.configure(background=color) 
	current_quad += 1

def penwidth():
	global current_quad, penWidth
	penwidth = quads[current_quad][1]
	current_quad += 1

def assign():
	global current_quad
	result = memory.getValue(quads[current_quad][1])
	print "ASS", result, " ", quads[current_quad][3] 
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def rectangle():
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	x2 = x + memory.getValue(quads[current_quad][1])
	y2 = y + memory.getValue(quads[current_quad][2])
	print "RECTANGLE ", x, " ", y, " ", x2, " ", y2, " ", fill 
	
	if(fill):
		w.create_rectangle(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_rectangle(x, y, x2, y2)
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def triangle():
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue(quads[current_quad][1])
	y = memory.getValue(quads[current_quad][2])
	current_quad += 1
	x2 = memory.getValue(quads[current_quad][0])
	y2 = memory.getValue(quads[current_quad][1])
	x3 = memory.getValue(quads[current_quad][2])
	y3 = memory.getValue(quads[current_quad][3])
	print "TRIANGLE ", x, " ", quads[current_quad][1] , " ", x2, " ", " ", fill 
	
	if(fill):
		w.create_polygon(x, y, x2, y2, x3, y3, fill=fillColor, outline=penColor, width=penWidth )	
	else:
		w.create_polygon(x, y, x2, y2, x3, y3, fill='', outline=penColor, width=penWidth )
	print quads[current_quad]
	current_quad += 1

def circle():
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	x2 = x + memory.getValue(quads[current_quad][1])
	y2 = y + memory.getValue(quads[current_quad][1])
	#print "CIRCLE ", x, " ", y, " ", x2, " ", y2, " ", fill 
	
	if(fill):
		w.create_oval(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_oval(x, y, x2, y2, fill='', outline=penColor, width=penWidth)
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def arc():
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	x2 = x + memory.getValue(quads[current_quad][1])
	y2 = y + memory.getValue(quads[current_quad][1])
	#print "CIRCLE ", x, " ", y, " ", x2, " ", y2, " ", fill 
	
	if(fill):
		w.create_arc(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_arc(x, y, x2, y2, fill='', outline=penColor, width=penWidth)
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def square():
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	x2 = x + memory.getValue(quads[current_quad][1])
	y2 = y + memory.getValue(quads[current_quad][1])
	print "SQUARE ", x, " ", y, " ", x2, " ", y2, " ", memory.getValue(quads[current_quad][1]) 
	
	if(fill):
		w.create_rectangle(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_rectangle(x, y, x2, y2, fill='', outline=penColor, width=penWidth)
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def linestrip():
	global current_quad, penWidth, penColor
	print quads[current_quad][2]
	dire = int(quads[current_quad][1])
	ren = int(quads[current_quad][2])
	points = []
	help = (memory.getValue('41000'), memory.getValue('41001'))
	points.append(help)
	cRen = 0
	print dire
	while cRen < ren:
		help = (memory.getValue(str(cRen + dire)), memory.getValue(str(cRen + 1 + dire)))
		points.append(help)
		cRen += 2
	print help
	w.create_line(points, fill=penColor)
	current_quad += 1

def polygon():
	global current_quad, penWidth, penColor
	print quads[current_quad][2]
	dire = int(quads[current_quad][1])
	ren = int(quads[current_quad][2])
	points = []
	help = (memory.getValue('41000'), memory.getValue('41001'))
	points.append(help)
	cRen = 0
	print dire
	while cRen < ren:
		help = (memory.getValue(str(cRen + dire)), memory.getValue(str(cRen + 1 + dire)))
		points.append(help)
		cRen += 2
	if(fill):
		w.create_polygon(points, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_polygon(points, fill='', outline=penColor, width=penWidth)
	current_quad += 1

def fill():
	global current_quad, fill
	#print "FILL ", quads[current_quad][3]
	if(quads[current_quad][3] == '1'):
		fill = True
	else:
		fill = False
	current_quad += 1

def get_x_and_y(angle, hypotenus):
	if(angle < 45):
		return [ hypotenus * (math.cos(math.radians(angle))), (-1 * (hypotenus * (math.sin(math.radians(angle)))))]
	elif(angle < 90):
		return [ hypotenus * (math.sin(math.radians(angle))), (-1 * (hypotenus * (math.cos(math.radians(angle)))))]
	elif(angle == 90):
		return [ 0, (-1*hypotenus)]

	angle -= 90
	if(angle < 45):
		return [ (-1 * (hypotenus * (math.sin(math.radians(angle))))), (-1 *  (hypotenus * (math.cos(math.radians(angle)))))]
	elif(angle < 90):
		return [ (-1 * (hypotenus * (math.cos(math.radians(angle))))), (-1 *  (hypotenus * (math.sin(math.radians(angle)))))]
	elif(angle == 90):
		return [(-1*hypotenus), 0]

	angle -= 90
	if(angle < 45):
		return [ (-1 * (hypotenus * (math.cos(math.radians(angle))))), hypotenus * (math.sin(math.radians(angle)))]
	elif(angle < 90):
		return [ (-1 * (hypotenus * (math.sin(math.radians(angle))))), hypotenus * (math.cos(math.radians(angle)))]
	elif(angle == 90):
		return [0, hypotenus]

	angle -= 90
	if(angle < 45):
		return [hypotenus * (math.sin(angle)), hypotenus * (math.cos(angle))]
	elif(angle < 90):
		return [hypotenus * (math.cos(angle)), hypotenus * (math.sin(angle))]	
	elif(angle == 90):
		return [hypotenus, 0]
	
def penpos():
	global current_quad
	memory.writeValue('41001', memory.getValue(quads[current_quad][1]))
	memory.writeValue('41000', memory.getValue(quads[current_quad][2]))
	current_quad += 1

def penX():
	global current_quad
	memory.writeValue('41000', memory.getValue(quads[current_quad][1]))
	current_quad += 1

def penY():
	global current_quad
	memory.writeValue('41001', memory.getValue(quads[current_quad][1]))
	current_quad += 1

def move():
	global current_quad, penColor
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	hyp = memory.getValue(quads[current_quad][1])
	angle = memory.getValue(quads[current_quad][2])
	pos = get_x_and_y(angle, hyp)
	print "X Y", pos[0], " ", pos[1]
	w.create_line(x, y,(x+pos[0]), (y+pos[1]), fill=penColor)
	current_quad += 1
	
def goto():
	global current_quad
	print "GOTO", current_quad
	current_quad = int(quads[current_quad][3])
	print quads[current_quad][3], "  ", current_quad

def goto_false():
	global current_quad
	temp = memory.getValue(quads[current_quad][1])
	if(temp):
		current_quad += 1
	else:
		current_quad = int(quads[current_quad][3])
	print "GOTOF", quads[current_quad][3], "  ", current_quad

def era():
	global current_quad
	temp = proc[quads[current_quad][3]]
	memory.setFunction(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
	current_quad += 1

def param():
	global current_quad
	print "PARAM ", quads[current_quad][3],  " ", memory.getValue(quads[current_quad][1])
	memory.writeValueS(quads[current_quad][3], memory.getValue(quads[current_quad][1]))
	current_quad += 1

def goSub():
	global current_quad
	memory.changeScope()
	actionPointer.push(current_quad+1)
	current_quad = int(quads[current_quad][3])

def return_f():
	global current_quad
	current_quad += 1

def dim():
	global current_quad
	value = memory.getValue(quads[current_quad][2])
	dim = int(quads[current_quad][1])
	if value < 0 or value > dim:
		print "Out of bounds."
		sys.exit(0)
	current_quad += 1

def dimC():
	global current_quad
	value = int(quads[current_quad][2])
	dim = int(quads[current_quad][1])
	if value < 0 or value > dim:
		print "Out of bounds."
		sys.exit(0)
	current_quad += 1

def pointerDir():
	global current_quad
	vDir = int(quads[current_quad][1])
	vPoint = memory.getValue(quads[current_quad][2])
	print "VDIR " , vDir+vPoint
	vDir = vDir + vPoint
	memory.writePointValue(quads[current_quad][3], str(vDir))
	current_quad += 1

def pointerDirC():
	global current_quad
	vDir = int(quads[current_quad][1])
	vPoint = int(quads[current_quad][2])
	print "VDIR " , vDir+vPoint
	vDir = vDir + vPoint
	memory.writePointValue(quads[current_quad][3], str(vDir))
	current_quad += 1

def endPro():
	global current_quad
	memory.printFunctions()
	current_quad = int(actionPointer.pop())
	memory.delete_function()
	memory.printFunctions()

def endProg():
	global run
	run = False	

options = { '+' : add,
		'-' : substract,
		'*' : multiply,
		'/' : divide,
		'<' : less_than,
		'>' : more_than,
		'<>' : different_than,
		'==' : equal_to,
		'GOTO': goto,
		'GOTOF' : goto_false,
		'ENDPROG': endProg,
		'CLR' : setColor,
		'101': assign,
		'201' : rectangle,
		'202' : triangle,
		'203' : circle,
		'204' : square,
		'205' : polygon,
		'206' : linestrip,
		'207' : arc,
		'209' : fill,
		'301' : pencolor,
		'302' : color,
		'303' : backColor,
		'304' : penwidth,
		'307' : penpos,
		'308' : penX,
		'309' : penY,
		'305' : move,
		'ERA' : era,
		'PARAMETRO' : param,
		'GOSUB' : goSub,
		'RET' : return_f,
		'RETURN' : param,
		'DIM' : dim,
		'DIMC' : dimC,
		'DIR' : pointerDir,
		'DIRC' : pointerDirC,
		'ENDPROC' : endPro}

if(len(sys.argv) > 1):
	if sys.argv[1] == "-f":
		print sys.argv[2]
		f = open(sys.argv[2], "r")
		count = 0.5
		s = f.readlines()
		string = ""
		for line in s:
			line = line.strip()
			if(line == '%%'):
				count += 1
			else:
				if(count <= 1):
					if(count == 1):
						info = line.split(' ')
						memory.writeValue(info[1], info[0])
					else:
						count += 0.5
						info = line.split(' ')
						memory.constSize(int(info[0]), int(info[1]))
				if(count == 2):
					info = line.split(' ')
					if(info[0] == 'main'):
						memory.setMainMem(info[1], info[2], info[3], info[4], info[5], info[6]) 
					elif(info[0] == 'globals'):
						memory.setGlobalMem(info[1], info[2], info[3], info[4], info[5], info[6])
					else:
						proc[info[0]] = [info[1], info[2], info[3], info[4], info[5], info[6]]
				if(count == 3):
					info = line.split(' ')
					sp = [info[0], info[1], info[2], info[3]]
					quads.append(sp)
					
			string += line
		root = Tk()
		print "const int float", len(quads)
		memory.constPrint()
		w = Canvas(root, width=600, height=480)
		w.configure(background='white')
		w.pack()
		actions()
		print "const int float"
		memory.constPrint()
		print "main"
		memory.printMain()
		print "global"
		memory.printGl()
		mainloop()
		
else:
    print "):"
