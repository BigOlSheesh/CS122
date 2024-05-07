import os.path
import os
import tkinter as tk
import customtkinter as ctk                # allows for more customization in gui display
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
import re
#------------google api imports needed to access email contents------------
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#window dimensions
windowWidth = 1024
windowLength = 1024

historyLog = ""

CLIENT_FILE = 'client_secret.json'
SCOPES = ['https://mail.google.com/']

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
    def __init__(self, frame, historyLog):
        self.frame = frame
        self.gmailObj = gAPI()
        self.historyLog = historyLog

        self.askPresetLabel = None
        self.comboBox = None
        self.askPresetLabel2 = None
        self.comboBox2 = None
        self.historyLogLabel = None

        self.runPresetButton = None
        self.createPresetButton = None
        self.editPresetButton = None
        self.savePresetButton = None                #note this widget will be placed/unplaced later, it is not initially shown
        self.cancelPresetButton = None              #note this widget will be placed/unplaced later, it is not initially shown
        self.deletePresetButton = None

        self.createEmailListButton = None
        self.editEmailListButton = None
        self.saveEmailListButton = None             #note this widget will be placed/unplaced later, it is not initially shown
        self.cancelEmailListButton = None           #note this widget will be placed/unplaced later, it is not initially shown
        self.deleteEmailListButton = None

        #user friendly buttons
        self.createSpecificationTextBox = None
        self.addToOperant = None
        self.addLabelIds = None
        self.removeLabelIds = None
        self.inLabel = None
        self.notInLabel = None
        self.hasAttachment = None 
        self.fromEmail = None
        self.toEmail = None
        self.ccEmail = None
        self.bccEmail = None
        self.subjectKeyword = None
        self.Keyword = None
        self.afterDate = None
        self.beforeDate = None
        self.olderThan = None
        self.newerThan = None
        self.leftParenthesisOperant = None
        self.andOperant = None
        self.orOperant = None
        self.slashOperant = None
        self.rightParenthesisOperant = None
        #----------------------

        self.presetSelectionTextBox = None
        self.emailSelectionTextBox  = None
        self.historyLogTextBox  = None
        
        self.customizeNodes()
        self.addNodes()
        

    def addNodes(self):                                     #margin of 20 for the sides and height     //start of the box height wise is 32 from edge (total height is 960)
        self.askPresetLabel.place(x = 508, y = 52)             
        self.comboBox.place(x = 508, y = 87)
        self.presetSelectionTextBox.place(x = 508, y = 141)
        self.createPresetButton.place(x = 508, y = 245)     #margin of 4 in between each button
        self.editPresetButton.place(x = 625, y = 245)
        self.deletePresetButton.place(x = 742, y = 245)
        self.runPresetButton.place(x = 859, y = 245) 

        self.askPresetLabel2.place(x = 508, y = 295)
        self.comboBox2.place(x = 508, y = 334)
        self.emailSelectionTextBox.place(x = 508, y = 388)
        self.createEmailListButton.place(x = 508, y = 492)      #margin of 4 in between each button
        self.editEmailListButton.place(x = 664, y = 492)
        self.deleteEmailListButton.place(x = 820, y = 492)

        self.historyLogLabel.place(x = 508, y = 542)
        self.historyLogTextBox.place(x = 508, y = 581)

    def customizeNodes(self):
        self.askPresetLabel = ctk.CTkLabel(master=self.frame, width = 464, height = 35, bg_color= "#282828",
                                           text_color= "white", font = ("Arial", 20), text = " P R E S E T ")
        self.comboBox = ctk.CTkComboBox(master=self.frame, width = 464, height = 50, corner_radius=10, bg_color= "#282828", fg_color="#3e3e3e", command=self.configurePresetTextBox,
                                        values = PresetManager.listFolderFileNames("presets"), state = "readonly", dropdown_hover_color="gray")
        self.askPresetLabel2 = ctk.CTkLabel(master=self.frame, width = 464, height = 35, bg_color= "#282828",
                                            text_color= "white", font = ("Arial", 20), text = " E M A I L ")
        self.comboBox2 = ctk.CTkComboBox(master=self.frame, width = 464, height = 50, corner_radius=10, bg_color= "#282828", fg_color="#3e3e3e", command=self.configureEmailTextBox,
                                        values = PresetManager.listFolderFileNames("emailList"), state = "readonly", dropdown_hover_color="gray")
        self.historyLogLabel = ctk.CTkLabel(master=self.frame, width = 464, height = 35, bg_color= "#282828",
                                           text_color= "white", font = ("Arial", 20), text = " H I S T O R Y ")

        self.runPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " R U N ", bg_color= "#282828", fg_color="#42513c", hover_color="#678c5a"
                                            , state = DISABLED, command=self.runPreset)
        self.createPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " C R E A T E ", bg_color= "#282828", fg_color="#3c4252", hover_color="#5a678c"
                                            , state = NORMAL, command=self.createNewPreset)
        self.editPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " E D I T ", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = DISABLED, command=self.editPreset)
        self.savePresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " S A V E ", bg_color= "#282828", fg_color="#42513c", hover_color="#678c5a"
                                            , state = NORMAL, command=self.savePreset)
        self.cancelPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " C A N C E L ", bg_color= "#282828", fg_color="#513c3c", hover_color="#8c5a5a"
                                            , state = NORMAL, command=self.cancelPreset)
        self.deletePresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " D E L E T E ", bg_color= "#282828", fg_color="#513c3c", hover_color="#8c5a5a"
                                            , state = DISABLED, command=self.deletePreset)

        self.createEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " C R E A T E ", bg_color= "#282828", fg_color="#3c4252", hover_color="#5a678c"
                                            , state = NORMAL, command=self.createNewEmailList)
        self.editEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " E D I T ", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = DISABLED, command=self.editEmailList)
        self.saveEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " S A V E ", bg_color= "#282828", fg_color="#42513c", hover_color="#678c5a"
                                            , state = NORMAL, command=self.saveEmailList)
        self.cancelEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " C A N C E L ", bg_color= "#282828", fg_color="#513c3c", hover_color="#8c5a5a"
                                            , state = NORMAL, command=self.cancelEmailList)
        self.deleteEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " D E L E T E ", bg_color= "#282828", fg_color="#513c3c", hover_color="#8c5a5a"
                                            , state = DISABLED, command=self.deleteEmailList)
        
        self.presetSelectionTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 100, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)         #will set state to normal when edit is pressed
        self.emailSelectionTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 100, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)          #will set state to normal when edit is pressed
        self.historyLogTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 385, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)              #will remain uneditable because it is history log

        #user friendly buttons
        self.createSpecificationTextBox = ctk.CTkTextbox(master=self.frame, width = 347, height = 38, bg_color= "#282828", fg_color="#3e3e3e", state = NORMAL)     #will remain editable (normal state)
        self.addToOperant = ctk.CTkButton(master=self.frame, width = 113, height = 38, text = "ADD", bg_color= "#282828", fg_color="#42513c", hover_color="#678c5a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, self.createSpecificationTextBox.get("0.0", END).rstrip()))
        self.addLabelIds = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "MOVE TO:", bg_color= "#282828", fg_color="#3c4252", hover_color="#5a678c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("addLabelIds: [YOUR, LABELS, HERE]"))
        self.removeLabelIds = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "REMOVE FROM:", bg_color= "#282828", fg_color="#3c4252", hover_color="#5a678c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("removeLabelIds: [YOUR, LABELS, HERE]"))
        self.inLabel = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " LABELED:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("in:"))
        self.notInLabel = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "NOT LABELED:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("-label:"))
        self.hasAttachment = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "ATTACHMENT", bg_color= "#282828", fg_color="#524f3c", hover_color="#8c855a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, "has:attachment"))
        self.fromEmail = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "FROM EMAIL:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("from:"))
        self.toEmail = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " TO EMAIL:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("to:"))
        self.ccEmail = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "CC EMAIL:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("cc:"))
        self.bccEmail = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "BCC EMAIL:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("bcc:"))
        self.subjectKeyword = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "SUBJECTLINE:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("subject:"))
        self.Keyword = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "KEYWORD:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox(""))
        self.afterDate = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "AFTER DATE:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("after:"))
        self.beforeDate = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "BEFORE DATE:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("before:"))
        self.olderThan = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "OLDER THAN:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("older_than:"))
        self.newerThan = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = "NEWER THAN:", bg_color= "#282828", fg_color="#3c5052", hover_color="#5a898c"
                                            , state = NORMAL, command=lambda: self.configureCreateSpecificationTextBox("newer_than:"))
        self.orOperant = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " OR ", bg_color= "#282828", fg_color="#524f3c", hover_color="#8c855a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, " OR "))
        self.andOperant = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " AND ", bg_color= "#282828", fg_color="#524f3c", hover_color="#8c855a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, " AND "))
        self.slashOperant = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " / ", bg_color= "#282828", fg_color="#524f3c", hover_color="#8c855a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, "/ "))
        self.leftParenthesisOperant = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " ( ", bg_color= "#282828", fg_color="#524f3c", hover_color="#8c855a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, "( "))
        self.rightParenthesisOperant = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " ) ", bg_color= "#282828", fg_color="#524f3c", hover_color="#8c855a"
                                            , state = NORMAL, command=lambda: self.presetSelectionTextBox.insert(END, " )"))
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------

    #when user selects something in the combobox under presets
    def configurePresetTextBox(self, fileName = ""):
        self.resetFunctions("preset", True, False)
        self.resetHistoryLog()

        contents = PresetManager.listPresets(fileName)
        if fileName != "PRESET_MANUAL(do not run)":
            self.presetSelectionTextBox.configure(state=NORMAL)
            self.presetSelectionTextBox.delete("0.0", END)
            self.presetSelectionTextBox.insert("0.0", contents)
            self.presetSelectionTextBox.configure(state=DISABLED)

            self.runPresetButton.configure(state = NORMAL)
            self.editPresetButton.configure(state = NORMAL)
            self.deletePresetButton.configure(state = NORMAL)
        else:
            self.historyLogLabel.configure(text = " P R E S E T  E X A M P L E ")
            self.historyLog = self.historyLogTextBox.get("0.0", END).rstrip()
            self.historyLogTextBox.configure(state=NORMAL)
            self.historyLogTextBox.delete("0.0", END)
            self.historyLogTextBox.insert("0.0", contents)
            self.historyLogTextBox.configure(state=DISABLED)

    #when user selects something in the combobox under email
    def configureEmailTextBox(self, fileName = ""):
        self.resetFunctions("email", True, False)
        self.resetHistoryLog()

        contents = EmailListManager.listEmails(fileName)
        if fileName != "EMAIL_MANUAL(do not run)":
            self.emailSelectionTextBox.configure(state=NORMAL)
            self.emailSelectionTextBox.delete("0.0", END)
            self.emailSelectionTextBox.insert("0.0", contents)
            self.emailSelectionTextBox.configure(state=DISABLED)

            self.editEmailListButton.configure(state = NORMAL)
            self.deleteEmailListButton.configure(state = NORMAL)
        else:
            self.historyLogLabel.configure(text = " E M A I L  E X A M P L E ")
            self.historyLog = self.historyLogTextBox.get("0.0", END).rstrip()
            self.historyLogTextBox.configure(state=NORMAL)
            self.historyLogTextBox.delete("0.0", END)
            self.historyLogTextBox.insert("0.0", contents)
            self.historyLogTextBox.configure(state=DISABLED)

    def configureHistoryLogTextBox(self, contentString):
        self.historyLogTextBox.configure(state=NORMAL)
        self.historyLogTextBox.insert(END, "\n" + contentString)
        self.historyLogTextBox.configure(state=DISABLED)
        self.historyLog = self.historyLogTextBox.get("0.0", END).rstrip()

    def configureCreateSpecificationTextBox(self, contentString):
        self.createSpecificationTextBox.delete("0.0", END)
        self.createSpecificationTextBox.insert("0.0", contentString)

    def hideEmailConfig(self):
        self.askPresetLabel2.place_forget()
        self.comboBox2.place_forget()
        self.emailSelectionTextBox.place_forget()
        self.createEmailListButton.place_forget()
        self.editEmailListButton.place_forget()
        self.deleteEmailListButton.place_forget()

    def showEmailConfig(self):
        self.askPresetLabel2.place(x = 508, y = 295)
        self.comboBox2.place(x = 508, y = 334)
        self.emailSelectionTextBox.place(x = 508, y = 388)
        self.createEmailListButton.place(x = 508, y = 492)      #margin of 4 in between each button
        self.editEmailListButton.place(x = 664, y = 492)
        self.deleteEmailListButton.place(x = 820, y = 492)

    def hideSpecificationConfig(self):
        self.createSpecificationTextBox.place_forget()
        self.addToOperant.place_forget()
        self.addLabelIds.place_forget()
        self.removeLabelIds.place_forget()
        self.inLabel.place_forget()
        self.notInLabel.place_forget()
        self.hasAttachment.place_forget()
        self.fromEmail.place_forget()
        self.toEmail.place_forget()
        self.ccEmail.place_forget()
        self.bccEmail.place_forget()
        self.subjectKeyword.place_forget()
        self.Keyword.place_forget()
        self.afterDate.place_forget()
        self.beforeDate.place_forget()
        self.olderThan.place_forget()
        self.newerThan.place_forget()
        self.leftParenthesisOperant.place_forget()
        self.andOperant.place_forget()
        self.orOperant.place_forget()
        self.slashOperant.place_forget()
        self.rightParenthesisOperant.place_forget()

    def showSpecificationConfig(self):
        self.createSpecificationTextBox.place(x = 508, y = 291)
        self.addToOperant.place(x = 859, y = 291)
        self.addLabelIds.place(x = 508, y = 334)
        self.removeLabelIds.place(x = 625, y = 334)
        self.inLabel.place(x = 742, y = 334)
        self.notInLabel.place(x = 859, y = 334)
        self.fromEmail.place(x = 508, y = 373)        
        self.toEmail.place(x = 625, y = 373)
        self.ccEmail.place(x = 742, y = 373)
        self.bccEmail.place(x = 859, y = 373)
        self.subjectKeyword.place(x = 508, y = 412)
        self.Keyword.place(x = 625, y = 412)
        self.afterDate.place(x = 742, y = 412)
        self.beforeDate.place(x = 859, y = 412)
        self.olderThan.place(x = 508, y = 451)
        self.newerThan.place(x = 625, y = 451)
        self.hasAttachment.place(x = 742, y = 451)
        self.leftParenthesisOperant.place(x = 859, y = 451)
        self.andOperant.place(x = 508, y = 490)
        self.orOperant.place(x = 625, y = 490)
        self.slashOperant.place(x = 742, y = 490)
        self.rightParenthesisOperant.place(x = 859, y = 490)

    #when user clicks create new preset
    def createNewPreset(self):
        self.resetFunctions("preset", True, True)
        self.hideEmailConfig()
        self.showSpecificationConfig()
        self.createPresetButton.place_forget()
        self.savePresetButton.place(x = 508, y = 245)
        self.editPresetButton.place_forget()
        self.cancelPresetButton.place(x = 625, y = 245)

        self.comboBox.configure(state = NORMAL)
        self.presetSelectionTextBox.configure(state = NORMAL)
        self.runPresetButton.configure(state = DISABLED)
        self.editPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)

    def deletePreset(self):
        PresetManager.deleteEntirePreset(self.comboBox.get())
        self.comboBox.configure(values=PresetManager.listFolderFileNames("presets"))
        self.resetFunctions("preset", True, True)
        self.showEmailConfig()
        self.hideSpecificationConfig()
        self.runPresetButton.configure(state = DISABLED)
        self.editPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)

    def editPreset(self):
        self.hideEmailConfig()
        self.showSpecificationConfig()

        self.createPresetButton.place_forget()
        self.savePresetButton.place(x = 508, y = 245)
        self.editPresetButton.place_forget()
        self.cancelPresetButton.place(x = 625, y = 245)

        self.comboBox.configure(state = NORMAL)
        self.presetSelectionTextBox.configure(state = NORMAL)

        self.createPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)
        self.runPresetButton.configure(state = DISABLED)

    def savePreset(self):
        self.savePresetButton.place_forget()
        self.createPresetButton.place(x = 508, y = 245)
        self.cancelPresetButton.place_forget()
        self.editPresetButton.place(x = 625, y = 245)

        title = self.comboBox.get()
        content = self.presetSelectionTextBox.get("0.0", END).rstrip()

        if self.createPresetButton.cget("state") == "normal":
            PresetManager.createPreset(title, content)
        elif self.editPresetButton.cget("state") == "normal":
            PresetManager.deleteEntirePreset(title)
            PresetManager.createPreset(title, content)

        self.comboBox.configure(values=PresetManager.listFolderFileNames("presets"))
        self.resetFunctions("preset", True, True)
        self.showEmailConfig()
        self.hideSpecificationConfig()
        self.resetHistoryLog()
        
    def cancelPreset(self):
        self.savePresetButton.place_forget()
        self.createPresetButton.place(x = 508, y = 245)
        self.cancelPresetButton.place_forget()
        self.editPresetButton.place(x = 625, y = 245)

        self.resetFunctions("preset", True, True)
        self.showEmailConfig()
        self.hideSpecificationConfig()
        self.resetHistoryLog()

    def runPreset(self):
        print("running")
        listOfPresets = PresetManager.listPresets(self.comboBox.get(), "list")
        if (len(listOfPresets) > 0):
            for preset in listOfPresets:
                print(preset)
                modifyRequestDict = {}
                query = ""
                listOfSpecifications = preset.strip().split("/ ")
                if (len(listOfSpecifications) > 1):
                    for specification in listOfSpecifications:
                        if "addLabelIds" in specification:
                            specification = specification.replace("addLabelIds: [", "").replace("]", "")
                            modifyRequestDict["addLabelIds"] = specification.split(", ")
                        elif "removeLabelIds" in specification:
                            specification = specification.replace("removeLabelIds: [", "").replace("]", "")
                            modifyRequestDict["removeLabelIds"] = specification.split(", ")
                        elif "labelIdsFrom" in specification:
                            specification = specification.replace("labelIdsFrom: [", "").replace("]", "")

                        else:
                            query = G.listEmailQuery(specification)
                self.configureHistoryLogTextBox("MODIFICATION REQUEST(S): " + str(modifyRequestDict) +
                                                "\nSPECIFICATION(S): " + str(query) +
                                                "\n- - - - - - - S T A R T  H E R E - - - - - - -")
                G.moveEmail(modifyRequestDict, G.searchEmails(query))


    def createNewEmailList(self):
        self.resetFunctions("email", True, True)
        self.createEmailListButton.place_forget()
        self.saveEmailListButton.place(x = 508, y = 492)
        self.editEmailListButton.place_forget()
        self.cancelEmailListButton.place(x = 664, y = 492)

        self.comboBox2.configure(state = NORMAL)
        self.emailSelectionTextBox.configure(state = NORMAL)
        self.editEmailListButton.configure(state = DISABLED)
        self.deleteEmailListButton.configure(state = DISABLED)

    def deleteEmailList(self):
        EmailListManager.deleteEntireEmailList(self.comboBox2.get())
        self.comboBox2.configure(values=PresetManager.listFolderFileNames("emailList"))
        self.resetFunctions("email", True, True)
        self.editEmailListButton.configure(state = DISABLED)
        self.deleteEmailListButton.configure(state = DISABLED)

    def editEmailList(self):
        self.createEmailListButton.place_forget()
        self.saveEmailListButton.place(x = 508, y = 492)
        self.editEmailListButton.place_forget()
        self.cancelEmailListButton.place(x = 664, y = 492)

        self.comboBox2.configure(state = NORMAL)
        self.emailSelectionTextBox.configure(state = NORMAL)

        self.createEmailListButton.configure(state = DISABLED)
        self.deleteEmailListButton.configure(state = DISABLED)
    
    def saveEmailList(self):
        self.saveEmailListButton.place_forget()
        self.createEmailListButton.place(x = 508, y = 492)
        self.cancelEmailListButton.place_forget()
        self.editEmailListButton.place(x = 664, y = 492)

        title = self.comboBox2.get()
        content = self.emailSelectionTextBox.get("0.0", END).rstrip()

        if self.createEmailListButton.cget("state") == "normal":
            EmailListManager.createEmailList(title, content)
        elif self.editEmailListButton.cget("state") == "normal":
            EmailListManager.deleteEntireEmailList(title)
            EmailListManager.createEmailList(title, content)

        self.comboBox2.configure(values=PresetManager.listFolderFileNames("emailList"))
        self.resetFunctions("email", True, True)
        self.resetHistoryLog()

    def cancelEmailList(self):
        self.saveEmailListButton.place_forget()
        self.createEmailListButton.place(x = 508, y = 492)
        self.cancelEmailListButton.place_forget()
        self.editEmailListButton.place(x = 664, y = 492)

        self.resetFunctions("email", True, True)
        self.resetHistoryLog()

    #helper method to reset the box values and buttons
    def resetFunctions(self, presetOrEmail, buttons, boxes):
        if presetOrEmail == "preset":
            if (boxes == True):
                self.comboBox.set("")
                self.comboBox.configure(state="readonly")
                self.presetSelectionTextBox.configure(state=NORMAL)
                self.presetSelectionTextBox.delete("0.0", END)
                self.presetSelectionTextBox.configure(state=DISABLED)

            if (buttons == True):
                self.createPresetButton.place(x = 508, y = 245)
                self.editPresetButton.place(x = 625, y = 245)
                self.deletePresetButton.place(x = 742, y = 245)
                self.runPresetButton.place(x = 859, y = 245)
                self.savePresetButton.place_forget()
                self.cancelPresetButton.place_forget()

                self.createPresetButton.configure(state=NORMAL)
                self.editPresetButton.configure(state=DISABLED)
                self.deletePresetButton.configure(state=DISABLED)
                self.runPresetButton.configure(state=DISABLED)
                self.savePresetButton.configure(state=NORMAL)
                self.cancelPresetButton.configure(state=NORMAL)

        elif presetOrEmail == "email":
            if (boxes == True):
                self.comboBox2.set("")
                self.comboBox2.configure(state="readonly")
                self.emailSelectionTextBox.configure(state=NORMAL)
                self.emailSelectionTextBox.delete("0.0", END)
                self.emailSelectionTextBox.configure(state=DISABLED)

            if (buttons == True):
                self.createEmailListButton.place(x = 508, y = 492)
                self.editEmailListButton.place(x = 664, y = 492)
                self.deleteEmailListButton.place(x = 820, y = 492)
                self.saveEmailListButton.place_forget()
                self.cancelEmailListButton.place_forget()

                self.createEmailListButton.configure(state=NORMAL)
                self.editEmailListButton.configure(state=DISABLED)
                self.deleteEmailListButton.configure(state=DISABLED)
                self.saveEmailListButton.configure(state=NORMAL)
                self.cancelEmailListButton.configure(state=NORMAL)

    def resetHistoryLog(self):
        self.historyLogLabel.configure(text = " H I S T O R Y ")
        self.historyLogTextBox.configure(state=NORMAL)
        self.historyLogTextBox.delete("0.0", END)
        self.historyLogTextBox.insert("0.0", self.historyLog)
        self.historyLogTextBox.configure(state=DISABLED)
            


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


class gAPI:

    #constructor
    def __init__(self):
        # Stores the access token which allows access to the API
        self.creds = None
        self.service = None  

    def resetToken(self):
        file_path = "token.json" 
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def checkAuthentication(self):
        try:
            if os.path.exists('client_secret.json'):
                if os.path.exists('token.json'):
                    self.creds = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json', SCOPES)

                # Otherwise, generete the token.json file
                if not self.creds or not self.creds.valid:
                    if self.creds and self.creds.expired and self.creds.refresh_token:
                        self.creds.refresh(Request())
                    else:
                        # Launches the authentication page 
                        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
                        # Creates the credentials object that will be the access token that allows the app to connect to Google APIs
                        self.creds = flow.run_local_server(port=0)
                    # Writes the access token
                    with open('token.json', 'w') as token:
                        token.write(self.creds.to_json())

                # define the API service 
                self.service = build('gmail', 'v1', credentials=self.creds)
            else:
                messagebox.showerror("FileNotFoundError", "Please generate and place a client_secret.json file in folder directory and relaunch application.")
        except Exception as e:  # Catch any authentication errors
            print("Authentication Error:", e)
            return False 
        return True 

    # Method to search for message IDs based on the query
    # returns a list of email ids that match the query
    def searchEmails(self, query, labelIds=None):
        all_message_ids = []
        next_page_token = None
        while True:
            # search for a list of messages with query
            message_list_response = self.service.users().messages().list(
                        userId='me',
                        q = query,
                        labelIds=labelIds,
                        pageToken=next_page_token
                    ).execute()
            
            # Gets the message IDs from message_list_response
            message_ids = [message['id'] for message in message_list_response.get('messages', [])]
            all_message_ids.extend(message_ids)

            # Checks if there are more pages (meaning more than 100 messages)
            next_page_token = message_list_response.get('nextPageToken')
            if not next_page_token:
                break

        print(str(len(all_message_ids)) + ' Total Messages using query: ' + query + ' Label: ' + str(labelIds))
        return all_message_ids

    def moveEmail(self, modifyRequest, messageIds):
        total_deleted = 0
        for message_id in messageIds:
            self.PF.configureHistoryLogTextBox(message_id + "has been moved.")
            self.service.users().messages().modify(userId='me', id=message_id, body=modifyRequest).execute()
        self.PF.configureHistoryLogTextBox("--------------------------------------------------------------------")
        messagebox.showinfo("OPERATION COMPLETE", str(len(messageIds)) + " messages have been moved successfully.")

    def listEmailQuery(self, query = ""):
        print(query)
        self.query = query + " "
        i = 0
        while i in range(len(self.query)):
            originalCommand = ""
            substring = ""
            orOrAnd = ""
            commandType = ""
            if self.query[i] == "f" and 0 <= i + 5 <= len(self.query):
                substring = self.query[i : i + 5]
                if "from:" in substring:
                    commandType = "from:"
                    substring = self.query[i : self.query.find(" ", i)]
            if self.query[i] == "t" and 0 <= i + 5 <= len(self.query):
                substring = self.query[i : i + 3]
                if "to:" in substring:
                    commandType = "to:"
                    substring = self.query[i : self.query.find(" ", i)]
            if self.query[i] == "c" and 0 <= i + 5 <= len(self.query):
                substring = self.query[i : i + 3]
                if "cc:" in substring:
                    commandType = "cc:"
                    substring = self.query[i : self.query.find(" ", i)]
            if self.query[i] == "b" and 0 <= i + 5 <= len(self.query):
                substring = self.query[i : i + 4]
                if "bcc:" in substring:
                    commandType = "bcc:"
                    substring = self.query[i : self.query.find(" ", i)]

            if substring != "" and commandType != "" and "@" not in substring:
                print("found")
                originalCommand = substring
                substring = substring.replace(commandType, "")
                orOrAnd = substring[0]
                substring = substring.replace(orOrAnd, "")

                if orOrAnd == "|":
                    orOrAnd = " OR "
                elif orOrAnd == "&":
                    orOrAnd = " AND "
                else:
                    messagebox.showerror("USER INPUT INVALID SYNTAX", "EmailList was chosen without specifying '|' or '&'. Please fix and try again.")

                if orOrAnd == " OR " or orOrAnd == " AND ":
                    listOfEmails = EmailListManager.listEmails(substring, "list")
                    newCommand = commandType + listOfEmails[0]
                    for email in listOfEmails[1:]:
                        newCommand = newCommand + orOrAnd + commandType + email
                    print("--> " + newCommand)
                    self.query = self.query.replace(originalCommand + " ", newCommand + " ")
                    i = i + len(newCommand)
                    print (i)
                else:
                    i+=1
            else:
                i+=1
        print(self.query)
        return self.query

    def onOpen(self):
        self.checkAuthentication()
        if os.path.exists('client_secret.json'):
            window.protocol("WM_DELETE_WINDOW", lambda: self.onClose())
            frame.pack(fill = tk.BOTH, expand = True)                #pack this onto the display
            self.PD = ProgramDisplay(window, frame, "background/background.png", "background/icon.ico")
            self.PF = ProgramFunction(frame, historyLog)
        else:
            window.destroy()

    def onClose(self):
        self.resetToken()
        window.destroy()








#--------------------------------------run program----------------------------------------
window = tk.Tk()                                         #main window
frame = ttk.Frame()                                      #main frame (add stuff here))
G = gAPI()                                          # on start ask for authentication before doing anything
G.onOpen()
window.mainloop()
#-----------------------------------------------------------------------------------------

