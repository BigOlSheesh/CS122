import os.path
import os
from tkinter import messagebox
from tkinter import *

class PresetManager:
    """Class will manage all modifications to a preset."""
    #constructor
    def __init__(self):
        pass


    def listFolderFileNames(folderPath):
        """Method will return a list of the file names found so user can select. This is a universally usable method for both email lists and presets."""
        try:
            fileNames = os.listdir(folderPath)        #returns a list of the names
            fileNames =[file[:-4] for file in fileNames if file.endswith(".txt")]
            return(fileNames)
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    def listPresets(fileName = "", stringOrList = None):
        """Method will lists all the contents of the file (presets  in the file) on gui display."""
        try:
            with open ("presets/" + fileName + ".txt", 'r') as file:                      #open filepath (read only)
                if stringOrList == "list":                                                #if we want a list then return a list
                    content = file.readlines()
                    content = [preset.rstrip("\n") for preset in content]
                    return(content)
                else:                                                                     #if we want a string then return a string
                    content = file.read()
                    return(content)
                
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")


    def createPreset(nameOfPreset = "", contents = ""):     
        """Method will create new txt asking for name of preset and the contents to hold."""
        if (nameOfPreset == "" or os.path.exists("presets/" + nameOfPreset + ".txt")):          #if the file name is empty or already exists then toss a pop up for user to know
            messagebox.showerror("Error", "File name is either empty or already exists.")
        else:                                                                                   #otherwise, create the file, storing its contents within
            with open("presets/" + nameOfPreset + ".txt", "w") as file:
                file.write(contents)


    def deleteEntirePreset(fileName):
        """Method will delete the entire txt saved on file of the specified file name."""
        if os.path.exists("presets/" + fileName + ".txt"):          #if the file actually exists then we delete; otherwise, throw a pop up for user to know.
            os.remove("presets/" + fileName + ".txt")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting entire preset was unsuccessful.")