### IMPORTS ###
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

### GLOBALS ###
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_creds():
    """
    This function generates credentials in the name of the user, 
    and saves it for next use 
    """ 
    # Generate token and allow the app to access the user's GDrive account
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def monitor(service, user_email):
    """
    This function constantly monitoring the user's Google Drive 
    to find exposed files and make them private 
    """ 
    # Keep track of the last checked file
    last_checked_file = None

    # Continuously check for new files
    while True:
        # Search query for public folders owned by the user
        query = "(visibility='anyoneWithLink' or visibility='anyoneCanFind') and 'me' in owners"
        try:
            results = service.files().list(q=query,
                                        fields='nextPageToken, '
                                        'files(id, name)'
                                        ).execute()
            files = results.get("files", [])
            for file in files:
                # Check if this file is a new file
                if last_checked_file is None or file["id"] != last_checked_file:
                    last_checked_file = file["id"]
                    # Extract visibility type
                    permissions = service.permissions().list(fileId=last_checked_file).execute()
                    visibility = permissions['permissions'][0]['id']

                    try:                
                        # Remove existing visibility
                        service.permissions().delete(fileId=last_checked_file, permissionId=visibility).execute()

                        # Change the visibility to the current user
                        new_permission = {'type': 'user', 'role': 'owner', 'emailAddress': user_email}
                        service.permissions().create(fileId=last_checked_file, body=new_permission, transferOwnership=True).execute()

                        # Notify about visibility change
                        print(f'Visibility for file {file["name"]} has been changed to PRIVATE from {visibility}.')
            
                    except HttpError as error:
                        print(f'{error}')

        except HttpError as error:
            print(f'{error}')

def main():
    # Generate credentials for the current user
    creds = get_creds()
    
    # create drive api client
    service = build('drive', 'v3', credentials=creds)

    # Get the email address of the current user
    about = service.about().get(fields='user').execute()
    user_email = about["user"]["emailAddress"]
    
    # Monitor the user's Drive
    monitor(service, user_email)

if __name__ == '__main__':
    main()