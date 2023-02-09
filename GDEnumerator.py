### IMPORTS ###
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

### GLOBALS ###
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

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

        # Search for public files
        query = "visibility='anyoneCanFind' or visibility='anyoneWithLink'"
        try:
            results = service.files().list(q=query,
                                            fields='nextPageToken, '
                                            'files(id, name, createdTime)'
                                            ).execute()
            files = results.get("files", [])
            for file in files:
                print(f'{file["name"]}, Created Time: {file["createdTime"]}')

        except HttpError as error:
            print(f'{error}')

    except HttpError as error:
        print(f'{error}')

if __name__ == '__main__':
    main()