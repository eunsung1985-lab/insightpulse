import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_result(name, success, message=""):
    icon = "[OK]" if success else "[FAIL]"
    print(f"{icon} {name}: {message}")

def test_imports():
    try:
        import flask
        import google.generativeai
        import googleapiclient
        import fpdf
        import feedparser
        print_result("Dependency Check", True, "All libraries imported successfully.")
        return True
    except ImportError as e:
        print_result("Dependency Check", False, f"Missing library: {e}")
        return False

def test_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or "AIza" not in api_key:
        print_result("Gemini API", False, "GOOGLE_API_KEY is missing or invalid in .env")
        return
    
    try:
        from services.gemini_service import gemini_service
        # Mocking the call to avoid using quota or if service initialized incorrectly
        if gemini_service.model:
            print_result("Gemini API", True, "Service initialized with API Key.")
        else:
            print_result("Gemini API", False, "Service failed to initialize.")
    except Exception as e:
        print_result("Gemini API", False, str(e))

def test_drive():
    # OAuth Mode Check
    if os.path.exists("token.json") or os.path.exists("client_secret.json"):
        pass
    else:
        print_result("Drive API", False, "Missing 'client_secret.json' for OAuth.")
        return

    folder = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    if not folder:
         print_result("Drive API", False, "GOOGLE_DRIVE_FOLDER_ID is missing in .env")
         return

    try:
        from services.drive_service import drive_service
        # Trigger auth if needed
        if drive_service.service:
             print_result("Drive API", True, "Service authenticated successfully (OAuth).")
        else:
             print_result("Drive API", False, "Service authentication failed.")
    except Exception as e:
        print_result("Drive API", False, str(e))

def test_pdf():
    try:
        from services.pdf_service import pdf_service
        # Create a dummy PDF
        path = pdf_service.create_report("TEST_TICKER", "This is a test report.")
        if os.path.exists(path):
            print_result("PDF Generation", True, f"PDF created at {path}")
            # cleanup
            os.remove(path)
        else:
            print_result("PDF Generation", False, "File not created.")
    except Exception as e:
         print_result("PDF Generation", False, str(e))

def test_news():
    try:
        from services.news_service import news_service
        news = news_service.get_latest_news()
        if isinstance(news, list) and len(news) > 0:
            print_result("News Service", True, f"Successfully fetched {len(news)} items.")
        else:
             print_result("News Service", False, "Fetched 0 items (check internet).")
    except Exception as e:
        print_result("News Service", False, str(e))

if __name__ == "__main__":
    print("--- InsightPulse AI System Check ---")
    if test_imports():
        test_gemini()
        test_drive()
        test_pdf()
        test_news()
    print("------------------------------------")
