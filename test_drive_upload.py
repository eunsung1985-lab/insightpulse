import os
from dotenv import load_dotenv

# Load env before imports that use it
load_dotenv()

from services.pdf_service import pdf_service
from services.drive_service import drive_service

def test_manual_upload():
    print("[START] Starting Manual Drive Upload Test...")
    
    # DEBUG INFO
    print(f"   [DEBUG] Folder ID: {drive_service.folder_id}")
    if drive_service.service:
        about = drive_service.service.about().get(fields="user").execute()
        print(f"   [DEBUG] Service Email: {about['user']['emailAddress']}")
        
        # Check Folder Permissions
        try:
            folder = drive_service.service.files().get(fileId=drive_service.folder_id, fields="name, capabilities").execute()
            print(f"   [DEBUG] Folder Name: {folder.get('name')}")
            print(f"   [DEBUG] Can Add Children: {folder.get('capabilities', {}).get('canAddChildren')}")
        except Exception as e:
            print(f"   [FAIL] ACCESS DENIED. Cannot read folder: {e}")


    # 1. Create a dummy PDF
    print("[1] Generating PDF...")
    ticker = "TEST_NEWS"
    content = """
    [BREAKING NEWS]
    This is a test document to verify Google Drive Upload.
    
    If you are reading this, the integration is working successfully!
    InsightPulse AI is ready to serve.
    """
    
    try:
        pdf_path = pdf_service.create_report(ticker, content)
        print(f"   [OK] PDF Created: {pdf_path}")
    except Exception as e:
        print(f"   [FAIL] PDF Creation Failed: {e}")
        return

    # 2. Upload to Drive
    print("[2] Uploading to Google Drive...")
    try:
        link, error = drive_service.upload_file(pdf_path, "InsightPulse_Test_Upload.pdf")
        
        if link:
            print(f"   [OK] Upload Success!")
            print(f"   PLEASE CHECK YOUR GOOGLE DRIVE FOLDER.")
            print(f"   Link: {link}")
        else:
            print(f"   [FAIL] Upload Failed: {error}")
            
    except Exception as e:
        print(f"   [FAIL] Error during upload: {e}")

if __name__ == "__main__":
    test_manual_upload()
