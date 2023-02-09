### IMPORTS ###
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def main():
    
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() 
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder'"}).GetList()
    for folder in file_list:
        folder_id = folder['id']
        # Search for files in the folder
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents"}).GetList()

        # Check the sharing status of each new file
        for file in file_list:
           if file['shared']:
                print(f"File: {file['title']} is publicly accessible. Changing to private.")
                file.DeletePermission({'role': 'reader', 'type': 'anyone'})
                print("File permission changed to private")

if __name__ == '__main__':
    main()