import os.path
import os
import tkinter as tk
import customtkinter as ctk                 # allows for more customization in gui display
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
#------------google api imports needed to access email contents------------
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class ProgramDisplay:
    #constructor
    def __init__(self, window, frame, backgroundPath, iconPath):
        self.window = window                             #define reference to main window
        self.frame = frame
        self.backgroundPath = backgroundPath             
        self.iconPath = iconPath
        self.setUpWindow(self.window, self.iconPath)              #call method to set up window details (header, size, etc.)
        self.setUpBackground(self.backgroundPath)          #call method to display background

    def setUpWindow(self, window, iconPath):
        window.title("EmailButler")
        window.resizable(False, False)
        window.geometry("1024x1024")
        window.iconbitmap(iconPath)

    def setUpBackground(self, backgroundPath):
        self.background = Image.open(backgroundPath)
        self.backgroundLoader = ImageTk.PhotoImage(self.background)
        self.backgroundLabel = tk.Label(self.frame,image = self.backgroundLoader, border = 0)
        self.backgroundLabel.place(x=0,y=0)          #do this instead of .pack() or else everything get's pushed down like a vbox


class ProgramFunction:
    #constructor
    def __init__(self, frame):
        self.frame = frame
        self.addNodes()

    def addNodes(self):
        self.style = ttk.Style()
        self.style.configure("CustomCombobox.TCombobox",
                fieldbackground="#00000000",  # Transparent background as hex code
                foreground="white")  # White text
        
        self.comboBox = ttk.Combobox(self.frame,style="CustomCombobox.TCombobox")
        self.comboBox['values'] = ("Option 1", "Option 2", "Option 3")
        self.comboBox.pack()

        self.label = ttk.Label(self.frame, text = "hello")
        self.label.pack()

        self.label2 = ttk.Label(self.frame, text = "hello")
        self.label2.pack()

        self.label3 = ttk.Label(self.frame, text = "hello")
        self.label3.pack()

        self.label4 = ttk.Label(self.frame, text = "hello")
        self.label4.pack()

        self.label5 = ttk.Label(self.frame, text = "hello")
        self.label5.pack()

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
frame = ttk.Frame()                       #main frame (add stuff here))
frame.pack(fill = tk.BOTH, expand = True)                #pack this onto the display

PD = ProgramDisplay(window, frame, "background/background2.png", "background/icon.ico")
PF = ProgramFunction(frame)
window.mainloop()
#-----------------------------------------------------------------------------------------

