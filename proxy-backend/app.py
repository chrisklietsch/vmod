from flask import Flask, request, Response, jsonify
import cloudscraper

app = Flask(__name__)
scraper = cloudscraper.create_scraper()

@app.route('/proxy/fetch')
def proxy_fetch():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': 'Keine URL angegeben'}), 400
    try:
        response = scraper.get(target_url)
        response.raise_for_status()
        # Gib den Content-Type der Originalantwort weiter, z.B. text/html
        content_type = response.headers.get('Content-Type', 'text/html')
        return Response(response.content, content_type=content_type)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
