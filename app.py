import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# The Dream Destinations (Synced with destinations.js)
DREAM_DESTINATIONS = [
    {
        "id": "goa",
        "name": "Goa",
        "location": "India",
        "startPrice": 2999,
        "vibe": "🌊 Beach vibes • Parties • Heritage",
        "category": "beach"
    },
    {
        "id": "manali",
        "name": "Manali",
        "location": "Himachal Pradesh",
        "startPrice": 2499,
        "vibe": "🏔️ Mountains • Adventure • Cafes",
        "category": "mountain"
    },
    {
        "id": "pondicherry",
        "name": "Pondicherry",
        "location": "Tamil Nadu",
        "startPrice": 1999,
        "vibe": "🇫🇷 French quarters • Serene beaches • Spiritual",
        "category": "heritage"
    }
    # ... more synced data ...
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/destinations')
def get_destinations():
    return jsonify(DREAM_DESTINATIONS)

@app.route('/api/budget/calculate', methods=['POST'])
def calculate_budget():
    data = request.json
    total = data.get('total', 50000)
    days = data.get('days', 5)
    
    return jsonify({
        "stay": total * 0.4,
        "food": total * 0.25,
        "travel": total * 0.25,
        "misc": total * 0.1,
        "daily_limit": total / days
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "dreamy", "service": "wanderlog-api"})

if __name__ == '__main__':
    # Use environment port for deployment (e.g. Render, Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
