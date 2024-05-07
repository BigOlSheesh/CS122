import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

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
