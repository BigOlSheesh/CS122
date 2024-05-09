import os.path
import os
from tkinter import messagebox
from tkinter import *

class EmailListManager:
    """Class will manage all modifications to an email list."""
    #constructor
    def __init__(self):
        pass


    def listEmails(fileName = "", stringOrList = None):
        """Method will lists all the contents of the file (presets  in the file) on gui display."""
        try:
            with open ("emailList/" + fileName + ".txt", 'r') as file:                      #open filepath (read only)
                if stringOrList == "list":                                                  #if we want a list then return a list
                    content = file.readlines()
                    content = [email.rstrip("\n") for email in content]
                    return(content)
                else:                                                                       #if we want a string then return a string
                    content = file.read()
                    return(content)
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")


    def createEmailList(nameOfEmailList = "", contents = ""):     
        """Method will create new txt asking for name of emaillist and the contents to hold."""
        if (nameOfEmailList == "" or os.path.exists("emailList/" + nameOfEmailList + ".txt")):          #if the file name is empty or already exists then toss a pop up for user to know
            messagebox.showerror("Error", "File name is either empty or already exists.")
        else:                                                                                           #otherwise, create the file, storing its contents within
            with open("emailList/" + nameOfEmailList + ".txt", "w") as file:
                file.write(contents)    #this assumes contents has "\n" indent and the end already  


    def deleteEntireEmailList(fileName):
        """Method will delete the entire txt saved on file of the specified file name."""
        if os.path.exists("emailList/" + fileName + ".txt"):          #if the file actually exists then we delete; otherwise, throw a pop up for user to know.
            os.remove("emailList/" + fileName + ".txt")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting entire emailList was unsuccessful.")

