import customtkinter as ctk                # allows for more customization in gui display
from tkinter import messagebox
from tkinter import *
import TheGAPI as gA
import ThePresetManager as PM
import TheEmailListManager as EM

class ProgramFunction:
    #constructor
    def __init__(self, frame, historyLog, G):
        self.frame = frame
        self.historyLog = historyLog
        self.G = G

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
                                        values = PM.PresetManager.listFolderFileNames("presets"), state = "readonly", dropdown_hover_color="gray")
        self.askPresetLabel2 = ctk.CTkLabel(master=self.frame, width = 464, height = 35, bg_color= "#282828",
                                            text_color= "white", font = ("Arial", 20), text = " E M A I L ")
        self.comboBox2 = ctk.CTkComboBox(master=self.frame, width = 464, height = 50, corner_radius=10, bg_color= "#282828", fg_color="#3e3e3e", command=self.configureEmailTextBox,
                                        values = PM.PresetManager.listFolderFileNames("emailList"), state = "readonly", dropdown_hover_color="gray")
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

        contents = PM.PresetManager.listPresets(fileName)
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

        contents = EM.EmailListManager.listEmails(fileName)
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
        PM.PresetManager.deleteEntirePreset(self.comboBox.get())
        self.comboBox.configure(values=PM.PresetManager.listFolderFileNames("presets"))
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
            PM.PresetManager.createPreset(title, content)
        elif self.editPresetButton.cget("state") == "normal":
            PM.PresetManager.deleteEntirePreset(title)
            PM.PresetManager.createPreset(title, content)

        self.comboBox.configure(values=PM.PresetManager.listFolderFileNames("presets"))
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
        listOfPresets = PM.PresetManager.listPresets(self.comboBox.get(), "list")
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
                            query = self.G.listEmailQuery(specification)
                    self.configureHistoryLogTextBox("MODIFICATION REQUEST(S): " + str(modifyRequestDict) +
                                                    "\nSPECIFICATION(S): " + str(query) +
                                                    "\n- - - - - - - S T A R T  H E R E - - - - - - -")
                    self.G.moveEmail(modifyRequestDict, self.G.searchEmails(query))
                else:
                    messagebox.showerror("Invalid Preset", "There was no modification request or there was no specification. Please fix and try again.")


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
        EM.EmailListManager.deleteEntireEmailList(self.comboBox2.get())
        self.comboBox2.configure(values=PM.PresetManager.listFolderFileNames("emailList"))
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
            EM.EmailListManager.createEmailList(title, content)
        elif self.editEmailListButton.cget("state") == "normal":
            EM.EmailListManager.deleteEntireEmailList(title)
            EM.EmailListManager.createEmailList(title, content)

        self.comboBox2.configure(values=PM.PresetManager.listFolderFileNames("emailList"))
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
            