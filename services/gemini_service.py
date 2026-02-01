import os
import google.generativeai as genai
import json

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Standard model for quick tasks
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            # Deep Research model for heavy analysis
            self.research_model = genai.GenerativeModel('deep-research-pro-preview-12-2025')
        else:
            self.model = None
            self.research_model = None
            print("Warning: GOOGLE_API_KEY not found.")

    def analyze_stock(self, ticker, persona):
        """
        Analyzes a stock using Deep Research model.
        """
        if not self.research_model:
            return f"{persona} Analysis: API Key missing."

        prompts = {
            "optimist": f"Conduct a deep research on {ticker} as an optimistic analyst. Focus on growth potential, market opportunities, and competitive advantages. Provide a detailed report. (Korean)",
            "critic": f"Conduct a deep research on {ticker} as a critical analyst. Focus on financial risks, market threats, and valuation concerns. Provide a detailed report. (Korean)",
            "neutral": f"Conduct a deep research on {ticker} as a neutral reviewer. Synthesize optimistic and critical views into a balanced investment thesis. (Korean)"
        }
        
        prompt = prompts.get(persona, prompts['neutral'])
        
        try:
            # Use research model for analysis
            response = self.research_model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback to standard model if research model fails (e.g. quota)
            try:
                print(f"Deep Research model failed: {e}. Falling back to Flash.")
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e2:
                return f"Error generating analysis: {str(e2)}"

    def recommend_stocks(self, theme):
        """
        Recommends stocks based on a theme.
        """
        if not self.model:
             return [{"name": "Mock Stock", "ticker": "000000", "reason": "API Key Missing"}]

        if not theme or theme.strip() == "":
            prompt = "Recommend 3 trending stocks based on recent major news, high search volume, and government policy announcements. Provide detailed reasons explaining why it is trending. Return JSON with name, ticker, reason, valuation, risk. (Translate all content to Korean)"
        else:
            prompt = f"Recommend 3 stocks related to '{theme}'. Provide detailed reasons for the recommendation. Return JSON with name, ticker, reason, valuation, risk. (Translate all content to Korean)"
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse JSON from response. Simple heuristic.
            text = response.text
            # Use a more robust parser in production. Here assuming well-formed JSON from strong prompt.
            start = text.find('[')
            end = text.rfind(']') + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
            return []
        except Exception as e:
            return []

    def analyze_link_content(self, title, content):
        """
        Analyzes the content of a news link to recommend stocks.
        Uses Flash model for speed.
        """
        if not self.model:
             return "Gemini API Not Configured"

        prompt = f"""
        Analyze the following news content and recommend related stocks (Korean or US).
        
        [Title]: {title}
        [Content]: {content[:2000]} (truncated)
        
        Provide recommendations in this structure (Answer in Korean):
        1. [Stock Name] (Ticker): Reason based on the news
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error analyzing link: {str(e)}"

gemini_service = GeminiService()
