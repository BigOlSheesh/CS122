import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# define the client file and scopes
CLIENT_FILE = 'client_secret.json'
SCOPES = ['https://mail.google.com/']

# Stores the access token which allows access to the API
creds = None

# If the token is created, this will tell the API 
# that our account is already authenticated
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Otherwise, generete the token.json file
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Launches the authentication page 
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
        # Creates the credentials object that will be the access token that allows the app to connect to Google APIs
        creds = flow.run_local_server(port=0)
    # Writes the access token
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# define the API service
service = build('gmail', 'v1', credentials=creds)

# Method to search for message IDs based on the query
def searchEmails(query, labelIds=None):
    all_message_ids = []
    next_page_token = None
    while True:
        # search for a list of messages with query
        message_list_response = service.users().messages().list(
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
def deleteEmailIndividually(message_ids):
    total_deleted = 0
    # Takes each individual message_id from the list 
    for message_id in message_ids:
        try:
            # Requests the API service to move the email that correlates with the message id to the trash
            service.users().messages().trash(
                userId='me',
                id = message_id
                ).execute()
            total_deleted += 1
        except Exception as e:
            print(f'Error deleting message with ID {message_id}: {e}')

    print(str(total_deleted) + ' Total Messages deleted')

# Method to move emails from trash to Inbox
def moveFromTrashToInbox(message_ids):
    for message_id in message_ids:
        # Removes the trash label and add a inbox label
        modify_request = {
            'removeLabelIds': ['TRASH'],
            'addLabelIds': ['INBOX']
        }
        # Requests the API service to modify the messages that correlate to the message id with the modify_request
        service.users().messages().modify(userId='me', id=message_id, body=modify_request).execute()
    print("Messages moved from trash to inbox successfully.")

# Method to search for message IDs beased on the query specifically in trash
def getMessageIDsInTrash(query):
    response = service.users().messages().list(userId='me', labelIds=['TRASH'], q=query).execute()
    message_ids = [message['id'] for message in response.get('messages', [])]
    print('Found: ' + str(len(message_ids)))
    return message_ids

# Test code, Remove later!
def test1():
    ids = searchEmails('from:SP22: CS-46B Sec 01 - Intro to Data Strc')
    deleteEmailIndividually(ids)

def undo():
    ids = searchEmails('from:SP22: CS-46B Sec 01 - Intro to Data Strc', 'TRASH')
    moveFromTrashToInbox(ids)
