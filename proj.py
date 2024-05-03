import os.path
import os
import tkinter as tk
import customtkinter as ctk                # allows for more customization in gui display
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
#------------google api imports needed to access email contents------------
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#window dimensions
windowWidth = 1024
windowLength = 1024

historyLog = ""

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
    def __init__(self, frame, gmailObj, historyLog):
        self.frame = frame
        self.gmailObj = gmailObj
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
        
        self.runPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " R U N ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = DISABLED, command=self.runPreset)
        self.createPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " C R E A T E ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = NORMAL, command=self.createNewPreset)
        self.editPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " E D I T ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = DISABLED, command=self.editPreset)
        self.savePresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " S A V E ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = NORMAL, command=self.savePreset)
        self.cancelPresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " C A N C E L ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = NORMAL, command=self.cancelPreset)
        self.deletePresetButton = ctk.CTkButton(master=self.frame, width = 113, height = 35, text = " D E L E T E ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = DISABLED, command=self.deletePreset)

        self.createEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " C R E A T E ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = NORMAL, command=self.createNewEmailList)
        self.editEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " E D I T ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = DISABLED, command=self.editEmailList)
        self.saveEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " S A V E ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = NORMAL, command=self.saveEmailList)
        self.cancelEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " C A N C E L ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = NORMAL, command=self.cancelEmailList)
        self.deleteEmailListButton = ctk.CTkButton(master=self.frame, width = 152, height = 35, text = " D E L E T E ", bg_color= "#282828", fg_color="#4c4c4c", hover_color="gray"
                                            , state = DISABLED, command=self.deleteEmailList)

        self.presetSelectionTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 100, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)         #will set state to normal when edit is pressed
        self.emailSelectionTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 100, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)          #will set state to normal when edit is pressed
        self.historyLogTextBox = ctk.CTkTextbox(master=self.frame, width = 464, height = 385, bg_color= "#282828", fg_color="#3e3e3e", state = DISABLED)              #will remain uneditable because it is history log

    #when user selects something in the combobox under presets
    def configurePresetTextBox(self, fileName = ""):
        self.resetFunctions("preset", True, False)
        self.resetHistoryLog()

        contents = PresetManager.listPresets(fileName)
        if fileName != "example+instructions(do not run)":
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
        if fileName != "example+instructions(do not run)":
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

    #when user clicks create new preset
    def createNewPreset(self):
        self.resetFunctions("preset", True, True)
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
        self.runPresetButton.configure(state = DISABLED)
        self.editPresetButton.configure(state = DISABLED)
        self.deletePresetButton.configure(state = DISABLED)

    def editPreset(self):
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
        self.resetHistoryLog()
        
    def cancelPreset(self):
        self.savePresetButton.place_forget()
        self.createPresetButton.place(x = 508, y = 245)
        self.cancelPresetButton.place_forget()
        self.editPresetButton.place(x = 625, y = 245)

        self.resetFunctions("preset", True, True)
        self.resetHistoryLog()

    def runPreset(self):
        listOfPresets = PresetManager.listPresets(self.comboBox.get(), "list")
        if (len(listOfPresets) > 0):
            #self.gmailObj.checkAuthentication()
            for preset in listOfPresets:
                print(preset)
                if "Move to trash [status] after [x] days:" in preset:
                    pass
                elif "Move to trash emails from user(s) [nameOfList]:" in preset:
                    pass



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
            #print(fileNames)
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
        # define the client file and scopes
        self.CLIENT_FILE = 'client_secret.json'
        self.SCOPES = ['https://mail.google.com/']
        # Stores the access token which allows access to the API
        self.creds = None
        self.service = None

    def checkAuthentication(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # Otherwise, generete the token.json file
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Launches the authentication page 
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_FILE, self.SCOPES)
                # Creates the credentials object that will be the access token that allows the app to connect to Google APIs
                self.creds = flow.run_local_server(port=0)
            # Writes the access token
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        # define the API service
        self.service = build('gmail', 'v1', credentials=self.creds)
    
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

        print(str(len(all_message_ids)) + ' Total Messages using query: ' + query + ' Lable: ' + str(labelIds))
        return all_message_ids

    # Method to delete emails based on a message id
    def deleteEmailIndividually(self,message_ids):
        total_deleted = 0
        # Takes each individual message_id from the list 
        for message_id in message_ids:
            try:
                # Requests the API service to move the email that correlates with the message id to the trash
                self.service.users().messages().trash(
                    userId='me',
                    id = message_id
                    ).execute()
                total_deleted += 1
            except Exception as e:
                print(f'Error deleting message with ID {message_id}: {e}')

        print(str(total_deleted) + ' Total Messages deleted')

    # Method to move emails from trash to Inbox
    def moveFromTrashToInbox(self,message_ids):
        for message_id in message_ids:
            # Removes the trash label and add a inbox label
            modify_request = {
                'removeLabelIds': ['TRASH'],
                'addLabelIds': ['INBOX']
            }
            # Requests the API service to modify the messages that correlate to the message id with the modify_request
            self.service.users().messages().modify(userId='me', id=message_id, body=modify_request).execute()
        print("Messages moved from trash to inbox successfully.")

            
            









#--------------------------------------run program----------------------------------------
window = tk.Tk()                                         #main window
frame = ttk.Frame()                       #main frame (add stuff here))
frame.pack(fill = tk.BOTH, expand = True)                #pack this onto the display
gmailObj = gAPI()
PD = ProgramDisplay(window, frame, "background/background.png", "background/icon.ico")
PF = ProgramFunction(frame, gmailObj, historyLog)
window.mainloop()
#-----------------------------------------------------------------------------------------

