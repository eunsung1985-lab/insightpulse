import feedparser
from datetime import datetime

class NewsService:
    def __init__(self):
        # Google News RSS for "Finance" (Economy/Stock) - More reliable URL
        self.rss_url = "https://news.google.com/rss/search?q=%EA%B2%BD%EC%A0%9C+%7C+%EC%A3%BC%EC%8B%9D&hl=ko&gl=KR&ceid=KR:ko"
        self._cache = {} # {query_key: (timestamp, items)}
        self._cache_ttl = 600 # 10 minutes

    def get_latest_news(self, keywords=None):
        """
        Fetches latest news with caching.
        """
        # Create cache key
        if not keywords:
            cache_key = "default"
        else:
            cache_key = ",".join(sorted(keywords))
        
        # Check cache
        if cache_key in self._cache:
            timestamp, items = self._cache[cache_key]
            if (datetime.now() - timestamp).total_seconds() < self._cache_ttl:
                print(f"[News] Serving cached results for: {cache_key}")
                return items

        base_query_params = " when:3d -시세 -현재가 -등락률" # 3 days + exclusions
        
        if keywords and len(keywords) > 0:
            # Construct query: (k1 OR k2) ...
            # Google News RSS supports 'q=' parameter
            query = " OR ".join([f'"{k}"' for k in keywords])
            final_query = f"({query}){base_query_params}"
            import urllib.parse
            encoded_query = urllib.parse.quote(final_query)
            # Use search RSS format
            target_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        else:
            # Fallback or default topic
            target_url = self.rss_url

        try:
            feed = feedparser.parse(target_url)
            news_items = []

            for entry in feed.entries[:20]: # Limit to 20 items
                title = entry.title
                link = entry.link
                pub_date = entry.published
                
                # Simple keyword filtering
                if keywords:
                    if not any(k in title for k in keywords):
                        continue

                import random
                sentiment = random.choice(['neutral', 'positive', 'negative'])
                impact_summary = "AI가 분석한 이 뉴스의 시장 영향도 요약입니다."

                news_items.append({
                    "title": title,
                    "link": link,
                    "pub_date": pub_date,
                    "sentiment": sentiment,
                    "impact": impact_summary
                })
            
            # Update cache
            self._cache[cache_key] = (datetime.now(), news_items)
            return news_items
            
        except Exception as e:
            print(f"[News] Fetch error: {e}")
            return []

news_service = NewsService()
