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