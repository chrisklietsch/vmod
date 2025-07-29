from flask import Flask, request, jsonify
import cloudscraper
from bs4 import BeautifulSoup

app = Flask(__name__)
scraper = cloudscraper.create_scraper()

@app.route('/proxy/search')
def proxy_search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Kein Suchbegriff angegeben'}), 400
    url = f"https://kinoger.com/suche/{query}"
    try:
        response = scraper.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        # Beispiel: Link-Selector an Zielseite anpassen
        for a in soup.select('div.movie a'):
            title = a.get_text(strip=True)
            href = a['href']
            results.append({'title': title, 'url': href})
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

