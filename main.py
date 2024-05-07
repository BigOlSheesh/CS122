import tkinter as tk
import TheGAPI as gA
from tkinter import ttk

#window dimensions
windowWidth = 1024
windowLength = 1024

historyLog = ""

CLIENT_FILE = 'client_secret.json'
SCOPES = ['https://mail.google.com/']

#--------------------------------------run program----------------------------------------
window = tk.Tk()                                         #main window
frame = ttk.Frame()                                      #main frame (add stuff here))
G = gA.gAPI(CLIENT_FILE, SCOPES)                                          # on start ask for authentication before doing anything
G.onOpen(window, frame, historyLog, G)
window.mainloop()
#-----------------------------------------------------------------------------------------