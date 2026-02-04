from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from services.news_service import news_service
from services.gemini_service import gemini_service
from services.drive_service import drive_service
from services.pdf_service import pdf_service
from services.keyword_service import keyword_service
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
# Use a static secret key for production (from .env) or a default for dev
app.secret_key = os.getenv("SECRET_KEY", "dev-key")

# Routes
@app.route('/')
def index():
    # Fetch news based on selected keyword or default
    keyword = request.args.get('keyword')
    if keyword:
        news_items = news_service.get_latest_news([keyword])
        current_keyword = keyword
    else:
        # If no keyword selected, use all user keywords or default
        user_keywords = keyword_service.get_keywords()
        news_items = news_service.get_latest_news(user_keywords)
        current_keyword = "전체"

    return render_template('index.html', 
                          news_items=news_items, 
                          keywords=keyword_service.get_keywords(),
                          current_keyword=current_keyword)

@app.route('/api/keywords', methods=['GET', 'POST', 'DELETE'])
def manage_keywords():
    if request.method == 'GET':
        return jsonify(keyword_service.get_keywords())
    
    data = request.json
    keyword = data.get('keyword')
    
    if request.method == 'POST':
        keyword_service.add_keyword(keyword)
        return jsonify({'success': True})
    
    if request.method == 'DELETE':
        keyword_service.remove_keyword(keyword)
        return jsonify({'success': True})

@app.route('/api/analyze_link', methods=['POST'])
def analyze_link():
    data = request.json
    url = data.get('url')
    
    try:
        # Simple scraping
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title and likely main content
        title = soup.title.string if soup.title else "No Title"
        # Heuristic: Find paragraphs
        paragraphs = soup.find_all('p')
        content = " ".join([p.get_text() for p in paragraphs])
        
        result = gemini_service.analyze_link_content(title, content)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/analysis')
def analysis():
    ticker = request.args.get('ticker', '005930') # Default to Samsung Electronics
    # In a real app, we would fetch analysis here or via AJAX
    return render_template('analysis.html', ticker=ticker)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    ticker = data.get('ticker')
    persona = data.get('persona', 'neutral')
    result = gemini_service.analyze_stock(ticker, persona)
    return jsonify({'result': result})

@app.route('/picks')
def picks():
    return render_template('picks.html')

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.json
    theme = data.get('theme')
    recommendations = gemini_service.recommend_stocks(theme)
    return jsonify({'recommendations': recommendations})

@app.route('/api/save_pdf', methods=['POST'])
def save_pdf():
    try:
        data = request.json
        ticker = data.get('ticker')
        content = data.get('content')
        
        if not ticker or not content:
            return jsonify({'success': False, 'message': "Missing ticker or content"})

        # Generate PDF
        pdf_path = pdf_service.create_report(ticker, content)
        
        # Upload to Drive
        link, error = drive_service.upload_file(pdf_path, f"{ticker}_report.pdf")
        
        if error:
            return jsonify({'success': False, 'message': error})
        
        return jsonify({'success': True, 'link': link})
        
    except Exception as e:
        import traceback
        traceback.print_exc() # Print to server logs
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
