import sys
import math
from Tkinter import *
from MemoryAdministrator import MemoryAdministrator
from stack import Stack


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
#function that runs while you haven't reached the end of the program
	while(run):
		#print "QUADS", quads[current_quad], " ", memory.getValue('40000')
		options[quads[current_quad][0]]()

def add():
#function that adds two numbers
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "ADD ", first, " + ", second, " IN ", quads[current_quad][3]  
	result = first + second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def substract():
#function that substracts two numbers
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " - ", second, " IN ", quads[current_quad][3]  
	result = first - second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def multiply():
#function that multiplies two numbers
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " * ", second, " IN ", quads[current_quad][3]  
	result = first * second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def divide():
#function that divides two numbers
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " / ", second, " = ", first/second, " IN ", quads[current_quad][3]  
	result = first / second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def less_than():
#function that compares if one number is less than another
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "LESSSS ", first, " / ", second, " = ", first<second, " IN ", quads[current_quad][3]  
	result = first < second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def more_than():
#function that compares if one number is more than another
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "MOREE ", first, " / ", second, " = ", first>second, " IN ", quads[current_quad][3]  
	result = first > second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def less_than_eq():
#function that compares if one number is less than or equal to another
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "LESSSS ", first, " / ", second, " = ", first<second, " IN ", quads[current_quad][3]  
	result = first <= second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def more_than_eq():
#function that compares if one number is more than or equal to another
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "MOREE ", first, " / ", second, " = ", first>second, " IN ", quads[current_quad][3]  
	result = first >= second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def different_than():
#function that compares if one number is different than another
	global current_quad
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "SUB ", first, " / ", second, " = ", first/second, " IN ", quads[current_quad][3]  
	result = first != second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def equal_to():
#function that compares if one number is equal to another
	global current_quad
	#print "EQUAL ", quads[current_quad]
	first = memory.getValue(quads[current_quad][1])
	second = memory.getValue(quads[current_quad][2])
	#print "                 Equal ", first, " / ", second, " =  IN ", quads[current_quad][3]  
	result = first == second
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def stringColor(red, green, blue):
#gets the hexadecimal string for the color
	red = int(red)
	if(red > 255):
		red = 255
	green = int(green)
	if(green > 255):
		green = 255
	blue = int(blue)
	if(blue > 255):
		blue = 255
	
	color = '#' + str(format(red, '02x')) + str(format(green, '02x')) + str(format(blue, '02x'))
	return color

def pencolor():
#changes the pen color
	global current_quad, penColor
	red = memory.getValue(quads[current_quad][1])
	green = memory.getValue(quads[current_quad][2])
	blue = memory.getValue(quads[current_quad][3])
	
	penColor = stringColor(red, green, blue)
	#print "PENCOLOR", penColor
	current_quad += 1

def color():
#changes the color of the fill
	global current_quad, fillColor
	red = memory.getValue(quads[current_quad][1])
	green = memory.getValue(quads[current_quad][2])
	blue = memory.getValue(quads[current_quad][3])
	
	fillColor = stringColor(red, green, blue)
	#print "PENCOLOR", fillColor
	current_quad += 1
	
def backColor():
#changes the background color
	global current_quad, penWidth
	red = memory.getValue(quads[current_quad][1])
	green = memory.getValue(quads[current_quad][2])
	blue = memory.getValue(quads[current_quad][3])
	
	color = stringColor(red, green, blue)
	w.configure(background=color) 
	current_quad += 1

def penwidth():
#changes the width of the pen
	global current_quad, penWidth
	penWidth = memory.getValue(quads[current_quad][1])
	current_quad += 1

def assign():
#assigns a value to a variable
	global current_quad
	result = memory.getValue(quads[current_quad][1])
	#print "ASS", result, " ", quads[current_quad][3] 
	memory.writeValue(quads[current_quad][3], result)
	current_quad += 1

def rectangle():
#creates a rectangle with the proper requirements, moves the pen to the lower right corner
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	#print "RECTANGLE ", x, " ", y, " ", memory.getValue(quads[current_quad][1]), " ", memory.getValue(quads[current_quad][2]), " ", fill 
	x2 = x + memory.getValue(quads[current_quad][1])
	y2 = y + memory.getValue(quads[current_quad][2])
	#print "RECTANGLE ", x, " ", y, " ", x2, " ", y2, " ", fill 
	
	if(fill):
		w.create_rectangle(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_rectangle(x, y, x2, y2, fill='', outline=penColor, width=penWidth )
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def triangle():
#creates a triangle with the proper requirements
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue(quads[current_quad][1])
	y = memory.getValue(quads[current_quad][2])
	current_quad += 1
	x2 = memory.getValue(quads[current_quad][0])
	y2 = memory.getValue(quads[current_quad][1])
	x3 = memory.getValue(quads[current_quad][2])
	y3 = memory.getValue(quads[current_quad][3])
	#print "TRIANGLE ", x, " ", quads[current_quad][1] , " ", x2, " ", " ", fill 
	
	if(fill):
		w.create_polygon(x, y, x2, y2, x3, y3, fill=fillColor, outline=penColor, width=penWidth )	
	else:
		w.create_polygon(x, y, x2, y2, x3, y3, fill='', outline=penColor, width=penWidth )
	memory.writeValue('41000', x3)
	memory.writeValue('41001', y3)
	current_quad += 1

def circle():
#creates a circle taking the curren position as its center, moves the pen to the lower right corner
	global current_quad, fill, fillColor, penColor, penWidth
	size = memory.getValue(quads[current_quad][1])
	x = memory.getValue('41000') - size
	y = memory.getValue('41001') - size
	x2 = x + (size * 2)
	y2 = y + (size * 2)
	#print "CIRCLE ", x, " ", y, " ", x2, " ", y2, " ", fill 
	
	if(fill):
		w.create_oval(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_oval(x, y, x2, y2, fill='', outline=penColor, width=penWidth)
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def arc():
#creates an arc taking the current position as its center, moves the pen to the lower right corner
	global current_quad, fill, fillColor, penColor, penWidth
	size = memory.getValue(quads[current_quad][1])
	x = memory.getValue('41000') - size
	y = memory.getValue('41001') - size
	x2 = x + (size * 2)
	y2 = y + (size * 2)
	#print "CIRCLE ", x, " ", y, " ", x2, " ", y2, " ", fill 
	
	if(fill):
		w.create_arc(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_arc(x, y, x2, y2, fill='', outline=penColor, width=penWidth, extent=size, style=ARC)
	y2 = y2 - size
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def square():
#creates a square with the proper requirements, moves the pen to the lower right corner
	global current_quad, fill, fillColor, penColor, penWidth
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	x2 = x + memory.getValue(quads[current_quad][1])
	y2 = y + memory.getValue(quads[current_quad][1])
	#print "SQUARE ", x, " ", y, " ", x2, " ", y2, " ", memory.getValue(quads[current_quad][1]) 
	if(fill):
		w.create_rectangle(x, y, x2, y2, fill=fillColor, outline=penColor, width=penWidth)	
	else:
		w.create_rectangle(x, y, x2, y2, fill='', outline=penColor, width=penWidth)
	memory.writeValue('41000', x2)
	memory.writeValue('41001', y2)
	current_quad += 1

def label():
#prints a text label
	global current_quad, penColor, penWidth
	finish = int(quads[current_quad][3])
	start = int(quads[current_quad][2])
	lenght = finish - start
	start = 0
	direction = int(quads[current_quad][1])
	word = ''
	while start <= lenght:
		constDir = direction + start
		constDir = str(constDir)
		#print "COONST", constDir
		word += memory.getValue(constDir)
		start += 1
	w.create_text(memory.getValue('41000'), memory.getValue('41001'), text=word, fill=penColor)
	current_quad += 1

def linestrip():
#creates a series of lines taking into account the current position
	global current_quad, penWidth, penColor
	dire = int(quads[current_quad][1])
	ren = int(quads[current_quad][2])
	points = []
	help = (memory.getValue('41000'), memory.getValue('41001'))
	points.append(help)
	cRen = 0
	while cRen < ren:
		help = (memory.getValue(str(cRen + dire)), memory.getValue(str(cRen + 1 + dire)))
		points.append(help)
		cRen += 2
	w.create_line(points, fill=penColor)
	current_quad += 1

def polygon():
#creates a polygon with the given coordenates with the proper requirements
	global current_quad, penWidth, penColor
	dire = int(quads[current_quad][1])
	ren = int(quads[current_quad][2])
	points = []
	help = (memory.getValue('41000'), memory.getValue('41001'))
	points.append(help)
	cRen = 0
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
#determines if the figure will have filling or not
	global current_quad, fill
	#print "FILL ", quads[current_quad][3]
	if(quads[current_quad][3] == '1'):
		fill = True
	else:
		fill = False
	current_quad += 1

def get_x_and_y(angle, hypotenus):
#detetrmines the end of the line, basic mathematics
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
#changes the pen position
	global current_quad
	memory.writeValue('41001', memory.getValue(quads[current_quad][1]))
	memory.writeValue('41000', memory.getValue(quads[current_quad][2]))
	current_quad += 1

def penX():
#changes the x of the pen position
	global current_quad
	memory.writeValue('41000', memory.getValue(quads[current_quad][1]))
	current_quad += 1

def penY():
#changes the y of the pen position
	global current_quad
	memory.writeValue('41001', memory.getValue(quads[current_quad][1]))
	current_quad += 1

def penUp():
#moves the y of the pen upwards
	global current_quad
	up = memory.getValue('41001') - memory.getValue(quads[current_quad][1])
	memory.writeValue('41001', up)
	current_quad += 1

def penDown():
#moves the y of the pen downwards
	global current_quad
	up = memory.getValue(quads[current_quad][1]) + memory.getValue('41001')
	memory.writeValue('41001', up)
	current_quad += 1

def penLeft():
#moves the x of the pen to the left
	global current_quad
	up = memory.getValue('41000') - memory.getValue(quads[current_quad][1])
	memory.writeValue('41000', up)
	current_quad += 1

def penRight():
#moves the x of the pen to the right
	global current_quad
	up = memory.getValue(quads[current_quad][1]) + memory.getValue('41000')
	memory.writeValue('41000', up)
	current_quad += 1

def move():
#creates a line, has to calculate the end position of the line.
	global current_quad, penColor
	x = memory.getValue('41000')
	y = memory.getValue('41001')
	hyp = memory.getValue(quads[current_quad][1])
	angle = memory.getValue(quads[current_quad][2])
	pos = get_x_and_y(angle, hyp)
	#print "X Y", pos[0], " ", pos[1]
	w.create_line(x, y,(x+pos[0]), (y+pos[1]), fill=penColor)
	memory.writeValue('41000', (x+pos[0]))
	memory.writeValue('41001', (y+pos[1]))
	current_quad += 1
	
def goto():
#changes the current_quad
	global current_quad
	#print "GOTO", current_quad
	current_quad = int(quads[current_quad][3])
	#print quads[current_quad][3], "  ", current_quad

def goto_false():
#if the condition is false changes the current_quad
	global current_quad
	temp = memory.getValue(quads[current_quad][1])
	if(temp):
		current_quad += 1
	else:
		current_quad = int(quads[current_quad][3])
	#print "GOTOF", quads[current_quad][3], "  ", current_quad

def era():
#creates the memory necesary for the function that is being called.
	global current_quad
	temp = proc[quads[current_quad][3]]
	#print "ERA", temp
	memory.setFunction(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6])
	current_quad += 1

def param():
#function that assigns the values that are being sent to the function, has to check if its a pointer to make the proper write call.
	global current_quad
	if quads[current_quad][3][1] == '7':
		#pointer
		memory.writePointValue(quads[current_quad][3], quads[current_quad][1], 1)
		#print "PARAM ", quads[current_quad][3],  " ", quads[current_quad][1]
	else:
		memory.writeValueS(quads[current_quad][3], memory.getValue(quads[current_quad][1]))
		#print "PARAM ", quads[current_quad][3],  " ", memory.getValue(quads[current_quad][1])
	current_quad += 1

def goSub():
#saves the current quad, position it will return to and changes the current scope and current quad.
	global current_quad
	memory.changeScope()
	memory.actionPointer_push(current_quad+1)
	current_quad = int(quads[current_quad][3])

def dim():
#arrays when you want to access a value form an array check if the square is not out of bounds.
	global current_quad
	value = memory.getValue(quads[current_quad][2])
	dim = int(quads[current_quad][1])
	if value < 0 or value > dim:
		print "Out of bounds.", value, " ", dim
		sys.exit(0)
	current_quad += 1

def dimC():
#matrix when you want to access a value form an matrix check if the square is not out of bounds.
	global current_quad
	value = int(quads[current_quad][2])
	dim = int(quads[current_quad][1])
	if value < 0 or value > dim:
		print "Out of bounds.", value, " ", dim
		sys.exit(0)
	current_quad += 1

def pointerDir():
#retrieve the direction of the value you want to access, if its a pointer you have to retrieve its real base direction and add the position you want. store the direction to the pointer.
	global current_quad
	#print "         POINTER", quads[current_quad]
	if quads[current_quad][1][1] == '7':
		vDir = memory.getValuePointer(quads[current_quad][1])
	#	print "                    POINTER", vDir
	else:
		vDir = int(quads[current_quad][1])
	vPoint = memory.getValue(quads[current_quad][2])
	#print "VDIR " , vDir+vPoint
	vDir = vDir + vPoint
	memory.writePointValue(quads[current_quad][3], str(vDir), 0)
	current_quad += 1

def pointerDirC():
#gets the direction for the value and stores it to the pointer
	global current_quad
	vDir = int(quads[current_quad][1])
	vPoint = int(quads[current_quad][2])
	#print "VDIR " , vDir+vPoint
	vDir = vDir + vPoint
	memory.writePointValue(quads[current_quad][3], str(vDir), 0)
	current_quad += 1

def endPro():
#ends the procedure that was running, deletes all its data and returns to the point where the function call was made
	global current_quad
	current_quad = int(memory.actionPointer_pop())
	memory.delete_function()

def endProg():
#you have reached the end of the program.
	global run
	run = False	

options = { '+' : add,
		'-' : substract,
		'*' : multiply,
		'/' : divide,
		'<' : less_than,
		'>' : more_than,
		'<=' : less_than_eq,
		'>=' : more_than_eq,
		'<>' : different_than,
		'==' : equal_to,
		'GOTO': goto,
		'GOTOF' : goto_false,
		'ENDPROG': endProg,
		'101': assign,
		'201' : rectangle,
		'202' : triangle,
		'203' : circle,
		'204' : square,
		'205' : polygon,
		'206' : linestrip,
		'207' : arc,
		'208' : label,
		'209' : fill,
		'301' : pencolor,
		'302' : color,
		'303' : backColor,
		'304' : penwidth,
		'307' : penpos,
		'308' : penX,
		'309' : penY,
		'305' : move,
		'310' : penUp,
		'311' : penDown,
		'312' : penLeft,
		'313' : penRight,
		'ERA' : era,
		'PARAMETRO' : param,
		'GOSUB' : goSub,
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
						memory.constSize(int(info[0]), int(info[1]), int(info[2]))
				if(count == 2):
					info = line.split(' ')
					if(info[0] == 'main'):
						memory.setMainMem(info[1], info[2], info[3], info[4], info[5], info[6], info[7]) 
					elif(info[0] == 'globals'):
						memory.setGlobalMem(info[1], info[2], info[3], info[4], info[5], info[6], info[7])
					else:
						proc[info[0]] = [info[1], info[2], info[3], info[4], info[5], info[6], info[7]]
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
