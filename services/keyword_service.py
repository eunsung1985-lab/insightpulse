import json
import os

KEYWORDS_FILE = "keywords.json"

class KeywordService:
    def __init__(self):
        self._ensure_file_exists()

    def _ensure_file_exists(self):
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
        with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(keywords, f, ensure_ascii=False)

keyword_service = KeywordService()
