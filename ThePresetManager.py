import os.path
import os
from tkinter import messagebox
from tkinter import *

class PresetManager:
    #constructor
    def __init__(self):
        pass

    def listFolderFileNames(folderPath):
        try:
            fileNames = os.listdir(folderPath)        #returns a list of the names
            fileNames =[file[:-4] for file in fileNames if file.endswith(".txt")]
            return(fileNames)
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    #lists all the contents of the file (presets  in the file) on gui display
    def listPresets(fileName = "", stringOrList = None):
        try:
            with open ("presets/" + fileName + ".txt", 'r') as file:                      #open filepath (read only)
                if stringOrList == "list":
                    content = file.readlines()
                    content = [preset.rstrip("\n") for preset in content]
                    return(content)
                else:
                    content = file.read()
                    return(content)
                
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    #creates new txt asking for name of preset
    def createPreset(nameOfPreset = "", contents = ""):     
        if (nameOfPreset == "" or os.path.exists("presets/" + nameOfPreset + ".txt")):
            messagebox.showerror("Error", "File name is either empty or already exists.")
        else:
            with open("presets/" + nameOfPreset + ".txt", "w") as file:
                file.write(contents)    #this assumes contents has "\n" indent and the end already

    #delete entire txt of the specified preset
    def deleteEntirePreset(fileName):
        if os.path.exists("presets/" + fileName + ".txt"):
            os.remove("presets/" + fileName + ".txt")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting entire preset was unsuccessful.")