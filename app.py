from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"
CATEGORIES = ['general', 'technology', 'sports', 'business', 'health', 'science', 'entertainment']

@app.route('/')
def index():
    category = request.args.get('category', 'general')
    query = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    params = {
        'apiKey': API_KEY,
        'pageSize': 9,
        'page': page
    }

    if query:
        params['q'] = query
    else:
        params['category'] = category
        params['country'] = 'us'

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get('status') != 'ok':
        return f"❌ Error fetching news: {data.get('message', 'Unknown error')}"

    articles = data.get('articles', [])
    return render_template('index.html', articles=articles, categories=CATEGORIES, selected=category, page=page, query=query)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    app.run(debug=True)
