import os.path
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *


class ProgramDisplay:
    #constructor
    def __init__(self, window, backgroundPath, iconPath):
        self.window = window                             #define reference to main window
        self.canvas = Canvas(self.window)                #create canvas for background
        self.backgroundPath = backgroundPath             
        self.iconPath = iconPath
        self.setUpWindow(self.window, self.iconPath)              #call method to set up window details (header, size, etc.)
        self.setUpBackground(self.canvas, self.backgroundPath)          #call method to display background

    def setUpWindow(self, window, iconPath):
        window.title("EmailButler")
        window.resizable(False, False)
        window.geometry("1024x1024")
        window.iconbitmap(iconPath)

    def setUpBackground(self, canvas, backgroundPath):
        self.img  = PhotoImage(file = backgroundPath)    #create image from received path
        canvas.config(width = 1024, height = 1024,                          #set on main window w/ size
                           bd = 0, highlightthickness=0, relief="ridge")         #removes white border and highlight focus       
        canvas.pack(fill = tk.BOTH, expand = True)
        canvas.create_image(0,0,image = self.img, anchor = NW)


class ProgramFunction:
    #constructor
    def __init__(self, frame):
        self.frame = frame

    def addNodes(self):
        self.comboBox = ttk.Combobox(self.frame)

    def customizeNodes(self):
        pass

class PresetManager:
    #constructor
    def __init__(self):
        pass

    #lists all the contents of the file (presets  in the file) on gui display
    def listPresets(self, fileName = ""):
        try:
            with open ("presets/" + fileName + ".txt", 'r') as file:                      #open filepath (read only)
                print(file.read())                                  #get content and print
                return(file)
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")
            
    #appends new specification(preset) to the specified preset file
    def addToPreset(self, newPreset = "", fileName = ""):
        if newPreset != "" and os.path.exists("presets/" + fileName + ".txt"):
            with open ("presets/" + fileName + ".txt", 'a') as file:
                file.write(newPreset + "\n")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    #creates new txt asking for name of preset
    def createPreset(self, nameOfPreset = "", contents = ""):     
        if (nameOfPreset == "" or os.path.exists("presets/" + nameOfPreset + ".txt")):
            messagebox.showerror("Error", "File name is either empty or already exists.")
        else:
            with open("presets/" + nameOfPreset + ".txt", "w") as file:
                file.write(contents)    #this assumes contents has "\n" indent and the end already
            messagebox.showinfo("Operation update", "Creating new preset \"" + nameOfPreset + "\" was successful.")

    #edit preset (not adding just choosing what to delete)
    def deletePreset(self, fileName, deleteContents = ""):
        if deleteContents != "" and os.path.exists("presets/" + fileName + ".txt"):
            with open ("presets/" + fileName + ".txt", 'r') as file:
                content = file.readlines()
            if deleteContents + "\n" in content:
                with open ("presets/" + fileName + ".txt", 'w') as file:
                    for line in content:
                        if deleteContents.lower() + "\n" != line.lower():
                            file.write(line)
                messagebox.showinfo("Operation update", "Updating preset (delete) within \"" + fileName + "\" was successful.")
            else:
                messagebox.showinfo("Operation update", "Specified content to delete within \"" + fileName + "\" wasn't found. No changes were made.")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting a specification was unsuccessful.")

    #delete entire txt of the specified preset
    def deleteEntirePreset(self, fileName):
        if os.path.exists("presets/" + fileName + ".txt"):
            os.remove("presets/" + fileName + ".txt")
            messagebox.showinfo("Operation update", "Deleting entire preset \"" + fileName + "\" was successful.")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting entire preset was unsuccessful.")


class EmailListManager:
    #constructor
    def __init__(self):
        pass

    #lists all the contents of the file (emails in the file) on gui display
    def listEmails(self, fileName = ""):
        try:
            with open ("emailList/" + fileName + ".txt", 'r') as file:                      #open filepath (read only)
                print(file.read())                                  #get content and print
                return(file)
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    #appends new specification(email) to the specified emailList file
    def addToEmailList(self, newEmail = "", fileName = ""):
        if newEmail != "" and os.path.exists("emailList/" + fileName + ".txt"):
            with open ("emailList/" + fileName + ".txt", 'a') as file:
                file.write(newEmail + "\n")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    #creates new txt asking for name of emailList
    def createEmailList(self, nameOfEmailList = "", contents = ""):     
        if (nameOfEmailList == "" or os.path.exists("emailList/" + nameOfEmailList + ".txt")):
            messagebox.showerror("Error", "File name is either empty or already exists.")
        else:
            with open("emailList/" + nameOfEmailList + ".txt", "w") as file:
                file.write(contents)    #this assumes contents has "\n" indent and the end already
            messagebox.showinfo("Operation update", "Creating new emailList \"" + nameOfEmailList + "\" was successful.")    

    #edit emailList (not adding just choosing what to delete)
    def deleteEmail(self, fileName, deleteContents = ""):
        if deleteContents != "" and os.path.exists("emailList/" + fileName + ".txt"):
            with open ("emailList/" + fileName + ".txt", 'r') as file:
                content = file.readlines()
            if deleteContents + "\n" in content:
                with open ("emailList/" + fileName + ".txt", 'w') as file:
                    for line in content:
                        if deleteContents.lower() + "\n" != line.lower():
                            file.write(line)
                messagebox.showinfo("Operation update", "Updating email (delete) within \"" + fileName + "\" was successful.")
            else:
                messagebox.showinfo("Operation update", "Specified content to delete within \"" + fileName + "\" wasn't found. No changes were made.")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting email was unsuccessful.")

    #delete entire txt of the specified emailList
    def deleteEntireEmailList(self, fileName):
        if os.path.exists("emailList/" + fileName + ".txt"):
            os.remove("emailList/" + fileName + ".txt")
            messagebox.showinfo("Operation update", "Deleting entire emailList \"" + fileName + "\" was successful.")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting entire emailList was unsuccessful.")


            
            









#--------------------------------------run program----------------------------------------
window = tk.Tk()                                         #main window
frame = ttk.Frame(master = window)                       #main frame (add stuff here))
PD = ProgramDisplay(window, "background/background2.png", "background/icon.ico")
PF = ProgramFunction(frame)
window.mainloop()
#-----------------------------------------------------------------------------------------


