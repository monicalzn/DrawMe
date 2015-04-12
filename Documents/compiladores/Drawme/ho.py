from Tkinter import *

root = Tk()
w = Canvas(root, width=600, height=480)
w.pack()
w.create_line(0, 0, 200, 100)
w.create_rectangle(0, 0, 88, 30)
mainloop()
