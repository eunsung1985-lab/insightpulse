import json
import os

from services.drive_service import drive_service

KEYWORDS_FILE = "keywords.json"

class KeywordService:
    def __init__(self):
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        # Try to download from Drive first
        try:
            file_id = drive_service.search_file(KEYWORDS_FILE)
            if file_id:
                print(f"[Keywords] Found remote file (ID: {file_id}), downloading...")
                success = drive_service.download_file(file_id, KEYWORDS_FILE)
                if success:
                    return
        except Exception as e:
            print(f"[Keywords] Drive sync error: {e}")

        # If not on drive or download failed, use local or defaults
        if not os.path.exists(KEYWORDS_FILE):
            with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(["반도체", "2차전지", "AI"], f, ensure_ascii=False) # Defaults

    def get_keywords(self):
        try:
            with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def add_keyword(self, keyword):
        keywords = self.get_keywords()
        if keyword not in keywords:
            keywords.append(keyword)
            self._save(keywords)
            return True
        return False

    def remove_keyword(self, keyword):
        keywords = self.get_keywords()
        if keyword in keywords:
            keywords.remove(keyword)
            self._save(keywords)
            return True
        return False

    def _save(self, keywords):
        # Save local
        with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(keywords, f, ensure_ascii=False)
        
        # Sync to Drive (Background task would be better, but blocking is safer for now)
        try:
            drive_service.upload_json(KEYWORDS_FILE, KEYWORDS_FILE)
            print("[Keywords] Synced to Drive")
        except Exception as e:
            print(f"[Keywords] Failed to sync to Drive: {e}")

keyword_service = KeywordService()
