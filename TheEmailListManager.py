import os.path
import os
from tkinter import messagebox
from tkinter import *

class EmailListManager:
    #constructor
    def __init__(self):
        pass

    #lists all the contents of the file (emails in the file) on gui display
    def listEmails(fileName = "", stringOrList = None):
        try:
            with open ("emailList/" + fileName + ".txt", 'r') as file:                      #open filepath (read only)
                if stringOrList == "list":
                    content = file.readlines()
                    content = [email.rstrip("\n") for email in content]
                    return(content)
                else:
                    content = file.read()
                    return(content)
        except FileNotFoundError:                                   #throw file not found error if invalid filepath
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found.")

    #creates new txt asking for name of emailList
    def createEmailList(nameOfEmailList = "", contents = ""):     
        if (nameOfEmailList == "" or os.path.exists("emailList/" + nameOfEmailList + ".txt")):
            messagebox.showerror("Error", "File name is either empty or already exists.")
        else:
            with open("emailList/" + nameOfEmailList + ".txt", "w") as file:
                file.write(contents)    #this assumes contents has "\n" indent and the end already  

    #delete entire txt of the specified emailList
    def deleteEntireEmailList(fileName):
        if os.path.exists("emailList/" + fileName + ".txt"):
            os.remove("emailList/" + fileName + ".txt")
        else:
            messagebox.showerror("FileNotFoundError", "Specified file cannot be found. Deleting entire emailList was unsuccessful.")

