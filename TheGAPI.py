import os
import TheEmailListManager as EM
import TheProgramFunction as PF
import TheProgramDisplay as PD
import tkinter as tk
from tkinter import messagebox
#------------google api imports needed to access email contents------------
from google.auth.transport.requests import Request
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class gAPI:

    #constructor
    def __init__(self, clientFile, scopes):
        # Stores the access token which allows access to the API
        self.creds = None
        self.service = None  
        self.CLIENT_FILE = clientFile
        self.SCOPES = scopes

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
                    self.creds = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json', self.SCOPES)

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
                    listOfEmails = EM.EmailListManager.listEmails(substring, "list")
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

    def onOpen(self, window, frame, historyLog,G):
        self.checkAuthentication()
        if os.path.exists('client_secret.json'):
            window.protocol("WM_DELETE_WINDOW", lambda: self.onClose(window))
            frame.pack(fill = tk.BOTH, expand = True)                #pack this onto the display
            self.PD = PD.ProgramDisplay(window, frame, "background/background.png", "background/icon.ico")
            self.PF = PF.ProgramFunction(frame, historyLog,G)
        else:
            window.destroy()

    def onClose(self, window):
        self.resetToken()
        window.destroy()