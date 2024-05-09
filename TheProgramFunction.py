import customtkinter as ctk                # allows for more customization in gui display
from tkinter import messagebox
from tkinter import *
import TheGAPI as gA
import ThePresetManager as PM
import TheEmailListManager as EM

class ProgramFunction:
    #constructor
    def __init__(self, frame, historyLog, G):
        """Constructor will create and automatically assign/place/customize all widgets in a referencable manner."""
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
        """Method will place all the initial visible nodes for the GUI upon launch."""
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
        """Method will customize all GUI widgets even if they aren't yet placed, assign their commands/function, and specifications for which are editable on launch."""
        #COMBO-BOXES AND LABELS
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

        #PRESET BUTTONS
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

        #EMAILLIST BUTTONS
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
        
        #TEXTBOXES
        self.presetSelectionTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 100, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)         #will set state to normal when edit is pressed
        self.emailSelectionTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 100, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)          #will set state to normal when edit is pressed
        self.historyLogTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 385, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)              #will remain uneditable because it is history log

        #user friendly buttons (BUTTON TEMPLATES)
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

    def configurePresetTextBox(self, fileName = ""):
        """Method is called when user selects something in the combobox under presets."""
        self.resetFunctions("preset", True, False)          #reset to default edit criteria of preset widgets
        self.resetHistoryLog()                              #update the history log if needed

        contents = PM.PresetManager.listPresets(fileName)
        if fileName != "PRESET_MANUAL(do not run)":         #ensure that the preset manual cannot be deleted by user for their own reference
            #update the preset section's textbox with the preset specifications on file if it isn't the manual selected
            self.presetSelectionTextBox.configure(state=NORMAL)             #allow editing, clear the textbox and add new contents, then lock it again from edit
            self.presetSelectionTextBox.delete("0.0", END)                  
            self.presetSelectionTextBox.insert("0.0", contents)
            self.presetSelectionTextBox.configure(state=DISABLED)
            #make it so that once a preset has been selected, let buttons to edit, delete and run be pressable
            self.runPresetButton.configure(state = NORMAL)
            self.editPresetButton.configure(state = NORMAL)
            self.deletePresetButton.configure(state = NORMAL)
        else:
            #replace the history log temporarily with the manual information on the GUI if manual is selected
            self.historyLogLabel.configure(text = " P R E S E T  E X A M P L E ")
            self.historyLog = self.historyLogTextBox.get("0.0", END).rstrip()           #make sure to rstrip any unneeded white space and indents before storing
            self.historyLogTextBox.configure(state=NORMAL)
            self.historyLogTextBox.delete("0.0", END)
            self.historyLogTextBox.insert("0.0", contents)
            self.historyLogTextBox.configure(state=DISABLED)


    def configureEmailTextBox(self, fileName = ""):
        """Method is called when user selects something in the combobox under email."""
        self.resetFunctions("email", True, False)          #reset to default edit criteria of email widgets
        self.resetHistoryLog()                             #update the history log if needed

        contents = EM.EmailListManager.listEmails(fileName)
        if fileName != "EMAIL_MANUAL(do not run)":         #ensure that the email manual cannot be deleted by user for their own reference
            #update the preset section's textbox with the email specifications on file if it isn't the manual selected
            self.emailSelectionTextBox.configure(state=NORMAL)              #allow editing, clear the textbox and add new contents, then lock it again from edit
            self.emailSelectionTextBox.delete("0.0", END)
            self.emailSelectionTextBox.insert("0.0", contents)
            self.emailSelectionTextBox.configure(state=DISABLED)
            #make it so that once a email list has been selected, let buttons to edit and delete be pressable
            self.editEmailListButton.configure(state = NORMAL)
            self.deleteEmailListButton.configure(state = NORMAL)
        else:
            #replace the history log temporarily with the manual information on the GUI if manual is selected
            self.historyLogLabel.configure(text = " E M A I L  E X A M P L E ")    
            self.historyLog = self.historyLogTextBox.get("0.0", END).rstrip()           #make sure to rstrip any unneeded white space and indents before storing
            self.historyLogTextBox.configure(state=NORMAL)
            self.historyLogTextBox.delete("0.0", END)
            self.historyLogTextBox.insert("0.0", contents)
            self.historyLogTextBox.configure(state=DISABLED)

    def configureHistoryLogTextBox(self, contentString):
        """Method will set the text for the history log textbox. The textbox should never be editable."""
        #update the historytext box with the recorded history log content
        self.historyLogTextBox.configure(state=NORMAL)              #allow editing, clear the textbox and add new contents, then lock it again from edit
        self.historyLogTextBox.insert(END, "\n" + contentString)
        self.historyLogTextBox.configure(state=DISABLED)
        self.historyLog = self.historyLogTextBox.get("0.0", END).rstrip()

    def configureCreateSpecificationTextBox(self, contentString):
        """Method will set the text for the button template textbox which previews what template the user clicked. The textbox should always be editable."""
        self.createSpecificationTextBox.delete("0.0", END)              #since textbox is always allow to edit, simply clear text and replace with new content
        self.createSpecificationTextBox.insert("0.0", contentString)

    def hideEmailConfig(self):
        """Method will hide all widgets from the email section of the GUI."""
        self.askPresetLabel2.place_forget()
        self.comboBox2.place_forget()
        self.emailSelectionTextBox.place_forget()
        self.createEmailListButton.place_forget()
        self.editEmailListButton.place_forget()
        self.deleteEmailListButton.place_forget()

    def showEmailConfig(self):
        """Method will show all widgets from the email section of the GUI."""
        self.askPresetLabel2.place(x = 508, y = 295)
        self.comboBox2.place(x = 508, y = 334)
        self.emailSelectionTextBox.place(x = 508, y = 388)
        self.createEmailListButton.place(x = 508, y = 492)      #margin of 4 in between each button
        self.editEmailListButton.place(x = 664, y = 492)
        self.deleteEmailListButton.place(x = 820, y = 492)

    def hideSpecificationConfig(self):
        """Method will hide all widgets from the button template section of the GUI."""
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
        """Method will show all widgets from the button template section of the GUI."""
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


    def createNewPreset(self):
        """Method will be called when user clicks create new preset."""
        self.resetFunctions("preset", True, True)                                                   #reset the preset section
        self.hideEmailConfig()                                                                      #hide the email section
        self.showSpecificationConfig()                                                              #show the button template section so user can customize
        #substitute the buttons with saved and cancel when user finishes creating
        self.createPresetButton.place_forget()                                                     
        self.savePresetButton.place(x = 508, y = 245)
        self.editPresetButton.place_forget()
        self.cancelPresetButton.place(x = 625, y = 245)

        #disable buttons when reseting preset where no preset has been selected
        self.comboBox.configure(state = NORMAL)
        self.presetSelectionTextBox.configure(state = NORMAL)
        self.runPresetButton.configure(state = DISABLED)
        self.editPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)

    def deletePreset(self):
        """Method will be called when user deletes a preset."""
        PM.PresetManager.deleteEntirePreset(self.comboBox.get())                                     #get the name of the preset file that user selected and call helper method to delete
        self.comboBox.configure(values=PM.PresetManager.listFolderFileNames("presets"))              #update the combobox menu to delete the deleted file from selection
        self.resetFunctions("preset", True, True)                                                    #reset the preset section
        self.showEmailConfig()                                                                       #reset the email section
        self.hideSpecificationConfig()                                                               #hide the button template section if user happened to be editing

        #disable buttons when reseting preset where no preset has been selected
        self.runPresetButton.configure(state = DISABLED)                                             
        self.editPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)

    def editPreset(self):
        """Method is called when user wants to edit a selected preset."""
        self.hideEmailConfig()                                                      #hide the email section
        self.showSpecificationConfig()                                              #instead show the button templates in its place for editing presets
        #substitute the buttons with saved and cancel when user finishes editing
        self.createPresetButton.place_forget()                                      
        self.savePresetButton.place(x = 508, y = 245)
        self.editPresetButton.place_forget()
        self.cancelPresetButton.place(x = 625, y = 245)

        #set the state to allow editing for preset file's name and contents
        self.comboBox.configure(state = NORMAL)                                    
        self.presetSelectionTextBox.configure(state = NORMAL)

        #disable buttons when editing preset that was selected
        self.createPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)
        self.runPresetButton.configure(state = DISABLED)

    def savePreset(self):
        """Method is called when user wants to save a preset upon modifying."""
        #substitute the buttons with create and edit when user finishes editing
        self.savePresetButton.place_forget()                                       
        self.createPresetButton.place(x = 508, y = 245)
        self.cancelPresetButton.place_forget()
        self.editPresetButton.place(x = 625, y = 245)

        #get the name of the combobox and contents from the textbox below
        title = self.comboBox.get()
        content = self.presetSelectionTextBox.get("0.0", END).rstrip()

        #if we are saving a preset that is already made (aka editing) then we just edit the contents of the file
        #if we are saving a preset that is new and unregistered (aka creating) then we create a new file then add the contents inside the file
        if self.createPresetButton.cget("state") == "normal":
            PM.PresetManager.createPreset(title, content)
        elif self.editPresetButton.cget("state") == "normal":
            PM.PresetManager.deleteEntirePreset(title)
            PM.PresetManager.createPreset(title, content)

        self.comboBox.configure(values=PM.PresetManager.listFolderFileNames("presets"))             #after saving, update the combobox with the modified or newly added preset file
        self.resetFunctions("preset", True, True)                                                   #reset the functions of the preset section
        self.showEmailConfig()                                                                      #display email again to original state
        self.hideSpecificationConfig()                                                              #hide the button template section after finish modifying 
        self.resetHistoryLog()                                                                      #refresh history log if any change was made from opening the manual
        
    def cancelPreset(self):
        """Method is called when user chooses to cancel modifying or creating a preset."""
        #substitute the buttons with create and edit when user finishes editing
        self.savePresetButton.place_forget()                                                        
        self.createPresetButton.place(x = 508, y = 245)
        self.cancelPresetButton.place_forget()
        self.editPresetButton.place(x = 625, y = 245)

        self.resetFunctions("preset", True, True)                                                   #reset the functions of the preset section
        self.showEmailConfig()                                                                      #display email again to original state
        self.hideSpecificationConfig()                                                              #hide the button template section after finish modifying 
        self.resetHistoryLog()                                                                      #refresh history log if any change was made from opening the manual

    def runPreset(self):
        """Method will run the selected preset and the requests specified within."""
        print("running")
        listOfPresets = PM.PresetManager.listPresets(self.comboBox.get(), "list")                   #first get all the requests in the file (account for multiple operations)
        if (len(listOfPresets) > 0):                                                                #only do anything it there is a request at all
            for preset in listOfPresets:                                                                      #iterate through the list of requests found
                print(preset)
                modifyRequestDict = {}
                query = ""
                listOfSpecifications = preset.strip().split("/ ")                                             #create a sub-list containg specifications from each request in the main list of requests
                if (len(listOfSpecifications) > 1):                                                           #only do anything if there are at least 2 specifications, otherwise it either lacks a query or modification request
                    for specification in listOfSpecifications:                                                         #iterate through the specifications
                        if "addLabelIds" in specification:                                                                  #move to
                            specification = specification.replace("addLabelIds: [", "").replace("]", "")
                            modifyRequestDict["addLabelIds"] = specification.split(", ")
                        elif "removeLabelIds" in specification:                                                             #remove from
                            specification = specification.replace("removeLabelIds: [", "").replace("]", "")
                            modifyRequestDict["removeLabelIds"] = specification.split(", ")
                        else:                                                                                               #anything else should be considered a query search
                            query = self.G.listEmailQuery(specification)                                                    #convert the list if there are any requests to look into a email list file
                    self.configureHistoryLogTextBox("MODIFICATION REQUEST(S): " + str(modifyRequestDict) +                  #log history start and end
                                                    "\nSPECIFICATION(S): " + str(query) +
                                                    "\n- - - - - - - S T A R T  H E R E - - - - - - -")
                    self.G.moveEmail(modifyRequestDict, self.G.searchEmails(query))                                         #perform the modification
                else:
                    messagebox.showerror("Invalid Preset", "There was no modification request or there was no specification. Please fix and try again.")        #if preset or requests had issue then signal user


    def createNewEmailList(self):
        """Method is called when user wants to create a new email list."""
        self.resetFunctions("email", True, True)                        #reset the email list of prior edits to being new list

        #substitute the buttons with save and cancel when user is creating
        self.createEmailListButton.place_forget()
        self.saveEmailListButton.place(x = 508, y = 492)
        self.editEmailListButton.place_forget()
        self.cancelEmailListButton.place(x = 664, y = 492)

        #set the states of what can be editable when user wants to create
        self.comboBox2.configure(state = NORMAL)
        self.emailSelectionTextBox.configure(state = NORMAL)
        self.editEmailListButton.configure(state = DISABLED)
        self.deleteEmailListButton.configure(state = DISABLED)

    def deleteEmailList(self):
        """Method is called when user wants to delete an email list."""
        EM.EmailListManager.deleteEntireEmailList(self.comboBox2.get())                         #call helper method and pass in the chosen email list file name
        self.comboBox2.configure(values=PM.PresetManager.listFolderFileNames("emailList"))      #update the new combobox menu after deleting
        self.resetFunctions("email", True, True)                                                #reset the email section back to normal
        self.editEmailListButton.configure(state = DISABLED)                                    #disable buttons since no list is now selected from clearing
        self.deleteEmailListButton.configure(state = DISABLED)

    def editEmailList(self):
        """Method is called when user wants to edit an email list."""
        #substitute the buttons with save and cancel when user is editing
        self.createEmailListButton.place_forget()
        self.saveEmailListButton.place(x = 508, y = 492)
        self.editEmailListButton.place_forget()
        self.cancelEmailListButton.place(x = 664, y = 492)

        self.comboBox2.configure(state = NORMAL)
        self.emailSelectionTextBox.configure(state = NORMAL)

        self.createEmailListButton.configure(state = DISABLED)
        self.deleteEmailListButton.configure(state = DISABLED)
    
    def saveEmailList(self):
        """Method is called when user wants to save edits to an email list."""
        #substitute the buttons with create and edit when user finishes editing
        self.saveEmailListButton.place_forget()
        self.createEmailListButton.place(x = 508, y = 492)
        self.cancelEmailListButton.place_forget()
        self.editEmailListButton.place(x = 664, y = 492)

        #get the name of the email list and content of the list
        title = self.comboBox2.get()
        content = self.emailSelectionTextBox.get("0.0", END).rstrip()

        #if user is creating then create new create a new list
        #if user is just editing then clear file and make a new one with the contents
        if self.createEmailListButton.cget("state") == "normal":
            EM.EmailListManager.createEmailList(title, content)
        elif self.editEmailListButton.cget("state") == "normal":
            EM.EmailListManager.deleteEntireEmailList(title)
            EM.EmailListManager.createEmailList(title, content)

        #reset all fields regarding emaillist and update the combobox menu after saving
        self.comboBox2.configure(values=PM.PresetManager.listFolderFileNames("emailList"))
        self.resetFunctions("email", True, True)
        self.resetHistoryLog()

    def cancelEmailList(self):
        """Method is called when user cancels modifying or creating an email list."""
        #substitute the buttons with create and edit when user wants to cancel
        self.saveEmailListButton.place_forget()
        self.createEmailListButton.place(x = 508, y = 492)
        self.cancelEmailListButton.place_forget()
        self.editEmailListButton.place(x = 664, y = 492)

        #reset the emaillist field and history log if manual had caused any changes
        self.resetFunctions("email", True, True)
        self.resetHistoryLog()

    #helper method to reset the box values and buttons
    def resetFunctions(self, presetOrEmail, buttons, boxes):
        """Method is called when an operation had been completed and a reset of the GUI is wanted for a specific section."""
        #if we want to reset the preset section back to how it was on launch and clear all fields then:
        if presetOrEmail == "preset":
            #if we want the textboxes to be reset
            if (boxes == True):
                self.comboBox.set("")
                self.comboBox.configure(state="readonly")
                self.presetSelectionTextBox.configure(state=NORMAL)
                self.presetSelectionTextBox.delete("0.0", END)
                self.presetSelectionTextBox.configure(state=DISABLED)
            #if we want the buttons to also be reset
            if (buttons == True):
                self.createPresetButton.place(x = 508, y = 245)
                self.editPresetButton.place(x = 625, y = 245)
                self.deletePresetButton.place(x = 742, y = 245)
                self.runPresetButton.place(x = 859, y = 245)
                self.savePresetButton.place_forget()
                self.cancelPresetButton.place_forget()
                #reset the state of each button
                self.createPresetButton.configure(state=NORMAL)
                self.editPresetButton.configure(state=DISABLED)
                self.deletePresetButton.configure(state=DISABLED)
                self.runPresetButton.configure(state=DISABLED)
                self.savePresetButton.configure(state=NORMAL)
                self.cancelPresetButton.configure(state=NORMAL)
        #else if we want to reset the email section back to how it was on launch and clear all fields then:
        elif presetOrEmail == "email":
            #if we want the textboxes to be reset
            if (boxes == True):
                self.comboBox2.set("")
                self.comboBox2.configure(state="readonly")
                self.emailSelectionTextBox.configure(state=NORMAL)
                self.emailSelectionTextBox.delete("0.0", END)
                self.emailSelectionTextBox.configure(state=DISABLED)
            #if we want the buttons to also be reset
            if (buttons == True):
                self.createEmailListButton.place(x = 508, y = 492)
                self.editEmailListButton.place(x = 664, y = 492)
                self.deleteEmailListButton.place(x = 820, y = 492)
                self.saveEmailListButton.place_forget()
                self.cancelEmailListButton.place_forget()
                #reset the state of each button
                self.createEmailListButton.configure(state=NORMAL)
                self.editEmailListButton.configure(state=DISABLED)
                self.deleteEmailListButton.configure(state=DISABLED)
                self.saveEmailListButton.configure(state=NORMAL)
                self.cancelEmailListButton.configure(state=NORMAL)

    def resetHistoryLog(self):
        """Method is called when we want to display the history log contents from a saved global variable."""
        self.historyLogLabel.configure(text = " H I S T O R Y ")
        self.historyLogTextBox.configure(state=NORMAL)                  #allow edit, delete the contents of textbox, add new content, and lock it from editing again
        self.historyLogTextBox.delete("0.0", END)
        self.historyLogTextBox.insert("0.0", self.historyLog)
        self.historyLogTextBox.configure(state=DISABLED)
            