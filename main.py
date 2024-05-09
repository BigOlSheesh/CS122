import tkinter as tk              
import TheGAPI as gA
from tkinter import ttk

#window dimensions
windowWidth = 1024
windowLength = 1024

historyLog = ""                                          

CLIENT_FILE = 'client_secret.json'                       #user must provide this file in the program's local folder for authentication purposes
SCOPES = ['https://mail.google.com/']                    #scope in accessing google's mail system

#--------------------------------------run program----------------------------------------
window = tk.Tk()                                         #main window
frame = ttk.Frame()                                      #main frame (add stuff here)
G = gA.gAPI(CLIENT_FILE, SCOPES)                         #initialize authetication process and start program once authenticated
G.onOpen(window, frame, historyLog, G)
window.mainloop()
#-----------------------------------------------------------------------------------------
