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
    """Class is made to authenticate, initialize launch when authenticated, modify user's email content through requests, traverse their email content, and securely logs out after every session."""
    
    def __init__(self, clientFile, scopes):
        """Constructor sets up credentials, service token, establish scope of operation, and record client file for authentication."""
        self.creds = None                           # Stores the access token which allows access to the API
        self.service = None  
        self.CLIENT_FILE = clientFile
        self.SCOPES = scopes

    def resetToken(self):
        """Method will remove the token created at the start of each session, effectively logging the user out after every session for security purposes. This requires them to log in and authenticate each time."""
        file_path = "token.json" 
        try:
            os.remove(file_path)                    #after searching for file, if found have OS remove the file from their pc; otherwise, do nothing when there is already no file.
        except FileNotFoundError:
            pass

    def checkAuthentication(self):
        """Method will create a credentials token each session when user authenticates their gmail login on their browser. This will also assign the value of the constructor variables for class usage throughout the session."""
        try:
            #first check if a client file exists (only files authorized and approved can be modifed for security purposes)
            if os.path.exists('client_secret.json'):            
                #check if there is already a token (there shouldn't be but if there were no token shall be created)
                #if there is, link the token to credentials, allowing the credentials to access a scope of operation.
                if os.path.exists('token.json'):
                    self.creds = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json', self.SCOPES)

                #if token wasn't available then credentials wasn't assigned nor is it valid, we must create a new token
                if not self.creds or not self.creds.valid:
                    #refresh to check if there are already credentials that are just expired
                    if self.creds and self.creds.expired and self.creds.refresh_token:
                        self.creds.refresh(Request())

                    #otherwise, there are no expired credentials then have user authenticates and create a new valid session
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_FILE, self.SCOPES)              # Launches the authentication page 
                        self.creds = flow.run_local_server(port=0)                          
                   
                    with open('token.json', 'w') as token:                                   # Writes the access token
                        token.write(self.creds.to_json())

                self.service = build('gmail', 'v1', credentials=self.creds)                  # define the API service 
            else:                           
                #if there is no premade client file then we must have the user create one to have access to modify using the API
                messagebox.showerror("FileNotFoundError", "Please generate and place a client_secret.json file in folder directory and relaunch application.")

        except Exception as e:  # Catch any authentication errors
            print("Authentication Error:", e)
            return False 
        return True 


    def searchEmails(self, query, labelIds=None):
        """Method to search for message IDs based on the query and returns a list of said message IDs for usage."""
        all_message_ids = []                 #list for storing 
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
        """Method will do the modifying of the user's email contents with the given modification requests and list of message IDs to operate on."""
        total_deleted = 0        #counter for how many were operated on
        for message_id in messageIds:
            #log the history of what actions were being made
            self.PF.configureHistoryLogTextBox(message_id + "has been moved.")
            #perform the operation in an iterative process of the provided list
            self.service.users().messages().modify(userId='me', id=message_id, body=modifyRequest).execute() 
        self.PF.configureHistoryLogTextBox("--------------------------------------------------------------------")
        messagebox.showinfo("OPERATION COMPLETE", str(len(messageIds)) + " messages have been moved successfully.")         #display update to signal completion


    def listEmailQuery(self, query = ""):
        """Method will set up the query for the user to be able to pass a list of emails to operate on rather than entering emails one at a time."""
        print(query)
        self.query = query + " "
        i = 0
        while i in range(len(self.query)):      #iterate through the entire query
            originalCommand = ""
            substring = ""
            orOrAnd = ""
            commandType = ""

            #when commandTypes such as "from:", "to:", "cc:", or "bcc:" are found
            #if found then record the proceeding lines until the next spacing (format rule)
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

            #check if see if the user entered an email or list, lists will not have "@" for the name as a requested rule for the user.
            #if user does make the list have "@" their list will not be validated for conversion and gmail's API will rule that no email as such will be found.
            if substring != "" and commandType != "" and "@" not in substring:
                originalCommand = substring
                substring = substring.replace(commandType, "")
                orOrAnd = substring[0]
                substring = substring.replace(orOrAnd, "")

                #record the specification if user wants the list to be conjunctive or disjunctive
                if orOrAnd == "|":
                    orOrAnd = " OR "
                elif orOrAnd == "&":
                    orOrAnd = " AND "
                # if their were found then throw an error for user to fix
                # we will not run any modfication requests on a whim or through a default setting as information is sensative
                else:
                    messagebox.showerror("USER INPUT INVALID SYNTAX", "EmailList was chosen without specifying '|' or '&'. Please fix and try again.")

                #if there is an operant of conjuctive or disjunctive found then get the list of emails, create the conversion and edit the query.
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
        """Method will launch the program GUI upon authorized."""
        self.checkAuthentication()

        #ensure that the client file is once again existing before launching (security measure)
        #otherwise, remove the GUI window to prevent unauthorized modifying
        if os.path.exists('client_secret.json'):
            #add security measure to delete the access token of the session upon closing the window (security measure)
            window.protocol("WM_DELETE_WINDOW", lambda: self.onClose(window))
            frame.pack(fill = tk.BOTH, expand = True)                #pack this onto the display
            self.PD = PD.ProgramDisplay(window, frame, "background/background.png", "background/icon.ico")      #sets up the looks of the GUI
            self.PF = PF.ProgramFunction(frame, historyLog,G)                                                   #sets up the widgets of the GUI for user interaction
        else:
            window.destroy()

    def onClose(self, window):
        """Method is used as a command for the main window's protocol."""
        self.resetToken()
        window.destroy()