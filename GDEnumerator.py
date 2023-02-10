### IMPORTS ###
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

### GLOBALS ###
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.metadata']

def change_scope(file):
    pass
def main():
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
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        # Get the email address of the current user
        about = service.about().get(fields='user').execute()
        user_email = about["user"]["emailAddress"]

        # Search for public files
        query = "mimeType='application/vnd.google-apps.folder' and (visibility='anyoneWithLink' or visibility='anyoneCanFind') and 'me' in owners"
        try:
            results = service.files().list(q=query,
                                            fields='nextPageToken, '
                                            'files(id, name, createdTime, mimeType)'
                                            ).execute()
            files = results.get("files", [])

            for file in files:
                file_id = file['id']
                
                # Extract visibility type
                permissions = service.permissions().list(fileId=file_id).execute()
                permissionid = permissions['permissions'][0]['id']

                try:                
                    # Remove existing visibility
                    service.permissions().delete(fileId=file_id, permissionId=permissionid).execute()

                    # Add a new permission with role 'owner'
                    new_permission = {'type': 'user', 'role': 'owner', 'emailAddress': user_email}
                    service.permissions().create(fileId=file_id, body=new_permission, transferOwnership=True).execute()

                    # Notify about permission change
                    print(f'Visibility for file {file["name"]} has been changed to PRIVATE from {permissionid}.')

                except HttpError as error:
                    print(f'{error}')

        except HttpError as error:
            print(f'{error}')

    except HttpError as error:
        print(f'{error}')

if __name__ == '__main__':
    main()