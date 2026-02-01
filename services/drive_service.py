from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

class DriveService:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
        self.creds = None
        self.service = None
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        
        self.authenticate()

    def authenticate(self):
        try:
            # Load existing token
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', self.scopes)
            
            # Refresh or Login
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if os.path.exists('client_secret.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'client_secret.json', self.scopes)
                        self.creds = flow.run_local_server(port=0)
                    else:
                        print("Warning: 'client_secret.json' not found. Drive uploads disabled.")
                        return

                # Save token
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())

            self.service = build('drive', 'v3', credentials=self.creds)
            print("[Drive] Authenticated successfully via OAuth.")
            
        except Exception as e:
            print(f"Error initializing Drive service (OAuth): {e}")

    def upload_file(self, file_path, file_name):
        """
        Uploads a file to Google Drive.
        """
        if not self.service:
            return None, "Drive service not initialized."

        try:
            file_metadata = {'name': file_name}
            if self.folder_id:
                file_metadata['parents'] = [self.folder_id]

            media = MediaFileUpload(file_path, mimetype='application/pdf')
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            return file.get('webViewLink'), None
        except Exception as e:
            return None, str(e)

drive_service = DriveService()
