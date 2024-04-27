from tkinter import ttk
from tkinter import *

class ProgramDisplay:

    #global variables go here ----------------------------------------------------------------


    #constructor
    def __init__(self, root):
        self.setUpRoot(root)
        self.setUpBackground(root)

    def setUpRoot(self, root):
        root.title("ZenMail")       #main window
        root.resizable(False, False)
        root.geometry("1024x1024")

    def setUpBackground(self, root):
        self.img = PhotoImage(file = "background/background.png")  
        canvas = Canvas(root, width = 1024, height = 1024)
        canvas.pack(fill = "both", expand = True)
        canvas.create_image(0,0,image = self.img, anchor = "nw")





#---------run program--------
root = Tk()
PD = ProgramDisplay(root)
root.mainloop()
#----------------------------


