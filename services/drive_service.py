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
            # [Cloud Fix] If token.json is missing but env var exists, create it
            env_token = os.getenv("GOOGLE_TOKEN_JSON")
            if not os.path.exists('token.json') and env_token:
                with open('token.json', 'w') as f:
                    f.write(env_token)
                print("[Drive] Restored token.json from Environment Variable")

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

    def search_file(self, filename):
        """Search for a file by name in the configured folder."""
        if not self.service: return None
        try:
            query = f"name = '{filename}' and trashed = false"
            if self.folder_id:
                query += f" and '{self.folder_id}' in parents"
            
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get('files', [])
            if files:
                return files[0]['id'] # Return first match
            return None
        except Exception as e:
            print(f"Drive Search Error: {e}")
            return None

    def download_file(self, file_id, local_path):
        """Download file content to local path."""
        if not self.service: return False
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            with open(local_path, 'wb') as f:
                f.write(fh.getvalue())
            return True
        except Exception as e:
            print(f"Drive Download Error: {e}")
            return False

    def update_file(self, file_id, local_path):
        """Update existing file content."""
        if not self.service: return False
        try:
            media = MediaFileUpload(local_path, resumable=True)
            self.service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            return True
        except Exception as e:
            print(f"Drive Update Error: {e}")
            return False
            
    def upload_json(self, local_path, filename):
        """Helper to upload/update JSON config file."""
        existing_id = self.search_file(filename)
        if existing_id:
            return self.update_file(existing_id, local_path)
        else:
            # Upload new
            try:
                file_metadata = {'name': filename}
                if self.folder_id:
                    file_metadata['parents'] = [self.folder_id]
                media = MediaFileUpload(local_path, mimetype='application/json')
                self.service.files().create(body=file_metadata, media_body=media).execute()
                return True
            except Exception as e:
                print(f"Drive Upload JSON Error: {e}")
                return False

drive_service = DriveService()
