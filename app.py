import os
import time
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ─── Amadeus Auth ────────────────────────────────────────────────────────────

AMADEUS_CLIENT_ID     = os.environ.get('AMADEUS_CLIENT_ID', '')
AMADEUS_CLIENT_SECRET = os.environ.get('AMADEUS_CLIENT_SECRET', '')
AMADEUS_BASE          = 'https://test.api.amadeus.com'   # swap to prod when ready

_token_cache = {'token': None, 'expires_at': 0}

def get_amadeus_token():
    """Returns a valid OAuth2 token, refreshing only when expired."""
    if _token_cache['token'] and time.time() < _token_cache['expires_at']:
        return _token_cache['token']

    if not AMADEUS_CLIENT_ID or AMADEUS_CLIENT_ID == 'your_api_key_here':
        return None   # No credentials configured — fall back to mock data

    try:
        r = requests.post(
            f'{AMADEUS_BASE}/v1/security/oauth2/token',
            data={
                'grant_type':    'client_credentials',
                'client_id':     AMADEUS_CLIENT_ID,
                'client_secret': AMADEUS_CLIENT_SECRET,
            },
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        _token_cache['token']      = data['access_token']
        _token_cache['expires_at'] = time.time() + data['expires_in'] - 60
        return _token_cache['token']
    except Exception as e:
        print(f'[Amadeus] Token error: {e}')
        return None


def amadeus_get(path, params=None):
    """Make an authenticated GET request to Amadeus API."""
    token = get_amadeus_token()
    if not token:
        return None
    try:
        r = requests.get(
            f'{AMADEUS_BASE}{path}',
            headers={'Authorization': f'Bearer {token}'},
            params=params,
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f'[Amadeus] Request error {path}: {e}')
        return None


# ─── Mock fallback data (always available) ───────────────────────────────────

MOCK_DESTINATIONS = [
    {
        "id": "goa",          "name": "Goa",
        "location": "India",  "lat": 15.2993, "lng": 74.1240,
        "image":     "https://images.unsplash.com/photo-1512343879784-960f40e07e7a?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1512343879784-960f40e07e7a?w=1200&h=600&fit=crop",
        "description": "Sun-kissed beaches, Portuguese heritage, and vibrant nightlife",
        "startPrice": 2999, "vibe": "🌊 Beach vibes • Parties • Heritage", "category": "beach",
        "iataCode": "GOI",
        "places": [
            {"name": "North Goa",  "image": "https://images.unsplash.com/photo-1589093019248-4d6dc9f7f8f3?w=400",
             "activities": ["Baga Beach", "Anjuna Flea Market", "Fort Aguada", "Saturday Night Market"]},
            {"name": "South Goa",  "image": "https://images.unsplash.com/photo-1512100354054-b6e6f5f0f4e8?w=400",
             "activities": ["Palolem Beach", "Butterfly Beach", "Colva Beach", "Dudhsagar Falls"]},
            {"name": "Panaji",     "image": "https://images.unsplash.com/photo-1586922251167-6c9e1ee7b8b3?w=400",
             "activities": ["Fontainhas", "Church of Our Lady", "Casino", "Latin Quarter"]},
        ]
    },
    {
        "id": "manali",       "name": "Manali",
        "location": "Himachal Pradesh", "lat": 32.2396, "lng": 77.1887,
        "image":     "https://images.unsplash.com/photo-1584191059421-638b2f94f471?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1584191059421-638b2f94f471?w=1200&h=600&fit=crop",
        "description": "Snow-capped peaks, pine forests, and adventure sports",
        "startPrice": 2499, "vibe": "🏔️ Mountains • Adventure • Cafes", "category": "mountain",
        "iataCode": "KUU",
        "places": [
            {"name": "Old Manali",   "image": "https://images.unsplash.com/photo-1626621341517-bbf1d9990a23?w=400",
             "activities": ["Cafe Hopping", "River Crossing", "Hiking", "Budget Stays"]},
            {"name": "Solang Valley","image": "https://images.unsplash.com/photo-1626621341517-bbf1d9990a23?w=400",
             "activities": ["Paragliding", "Snow Sports", "Zorbing", "Cable Car"]},
            {"name": "Rohtang Pass", "image": "https://images.unsplash.com/photo-1626621341517-bbf1d9990a23?w=400",
             "activities": ["Snow Activities", "Photography", "Bike Rides", "Snow Fighting"]},
        ]
    },
    {
        "id": "jaipur",       "name": "Jaipur",
        "location": "Rajasthan", "lat": 26.9124, "lng": 75.7873,
        "image":     "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=1200&h=600&fit=crop",
        "description": "The Pink City's royal heritage and majestic forts",
        "startPrice": 3499, "vibe": "🏰 Palaces • Forts • Colors", "category": "heritage",
        "iataCode": "JAI",
        "places": [
            {"name": "Amer Fort",   "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400",
             "activities": ["Elephant Ride", "Light Show", "Palace Tour", "Mirror Palace"]},
            {"name": "City Palace", "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400",
             "activities": ["Museum", "Royal Costumes", "Courtyards", "Art Gallery"]},
            {"name": "Hawa Mahal",  "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400",
             "activities": ["Photography", "Market Shopping", "Sunset Views", "Local Food"]},
        ]
    },
    {
        "id": "rishikesh",    "name": "Rishikesh",
        "location": "Uttarakhand", "lat": 30.0869, "lng": 78.2676,
        "image":     "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=1200&h=600&fit=crop",
        "description": "Yoga capital, river rafting, and spiritual vibes",
        "startPrice": 1499, "vibe": "🧘 Spiritual • Rafting • Cafes", "category": "spiritual",
        "iataCode": "DED",
        "places": [
            {"name": "Laxman Jhula", "image": "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400",
             "activities": ["Temples", "Cafes", "Ganga Aarti", "Shopping"]},
            {"name": "Shivpuri",     "image": "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400",
             "activities": ["River Rafting", "Camping", "Bungee Jumping", "Beach Volleyball"]},
            {"name": "Triveni Ghat", "image": "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400",
             "activities": ["Evening Aarti", "Meditation", "Sunset", "Photography"]},
        ]
    },
    {
        "id": "ladakh",       "name": "Ladakh",
        "location": "J&K",   "lat": 34.1526, "lng": 77.5771,
        "image":     "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=1200&h=600&fit=crop",
        "description": "Land of high passes — dramatic landscapes and Buddhist culture",
        "startPrice": 5999, "vibe": "🏍️ Adventure • Monasteries • Moonscapes", "category": "adventure",
        "iataCode": "IXL",
        "places": [
            {"name": "Pangong Lake", "image": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
             "activities": ["Camping", "Star Gazing", "Photography", "Paddle Boating"]},
            {"name": "Nubra Valley", "image": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
             "activities": ["Double Hump Camel", "Sand Dunes", "Monasteries", "Hot Springs"]},
            {"name": "Khardung La",  "image": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
             "activities": ["Highest Motorable Road", "Snow", "Photography", "Bike Ride"]},
        ]
    },
]


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/destinations')
def get_destinations():
    """Returns curated destinations (mock data enriched with live prices)."""
    destinations = [d.copy() for d in MOCK_DESTINATIONS]

    token = get_amadeus_token()
    if token:
        # Optionally enrich each destination with live inspiration data
        for dest in destinations:
            live = amadeus_get('/v1/shopping/flight-destinations', {
                'origin':      'DEL',
                'destination': dest.get('iataCode', ''),
                'maxPrice':    20000,
            })
            if live and live.get('data'):
                price = live['data'][0].get('price', {}).get('total')
                if price:
                    dest['livePrice'] = float(price)
                    dest['startPrice'] = int(float(price))

    return jsonify(destinations)


@app.route('/api/flights/search')
def search_flights():
    """Live flight search via Amadeus."""
    origin      = request.args.get('origin', 'DEL')
    destination = request.args.get('destination', 'GOI')
    date        = request.args.get('date', '2025-06-01')
    adults      = request.args.get('adults', '1')

    data = amadeus_get('/v2/shopping/flight-offers', {
        'originLocationCode':      origin,
        'destinationLocationCode': destination,
        'departureDate':           date,
        'adults':                  adults,
        'currencyCode':            'INR',
        'max':                     5,
    })

    if not data:
        return jsonify({'error': 'Flight data unavailable', 'mock': True,
                        'results': [{'price': {'total': '3499'}, 'mock': True}]}), 200

    # Slim down the response for the frontend
    results = []
    for offer in data.get('data', []):
        results.append({
            'price':    offer['price']['grandTotal'],
            'currency': offer['price']['currency'],
            'segments': [
                {
                    'departure':   seg['departure']['iataCode'],
                    'arrival':     seg['arrival']['iataCode'],
                    'departureAt': seg['departure']['at'],
                    'arrivalAt':   seg['arrival']['at'],
                    'carrier':     seg.get('carrierCode', ''),
                    'duration':    seg.get('duration', ''),
                }
                for itinerary in offer['itineraries']
                for seg in itinerary['segments']
            ],
        })

    return jsonify({'results': results, 'live': True})


@app.route('/api/hotels/search')
def search_hotels():
    """Live hotel search via Amadeus."""
    city_code = request.args.get('cityCode', 'GOA')
    check_in  = request.args.get('checkIn',  '2025-06-01')
    check_out = request.args.get('checkOut', '2025-06-05')
    adults    = request.args.get('adults',   '1')

    # Step 1: get hotel IDs by city
    hotels_by_city = amadeus_get('/v1/reference-data/locations/hotels/by-city', {
        'cityCode': city_code,
    })

    if not hotels_by_city:
        return jsonify({'error': 'Hotel data unavailable', 'mock': True,
                        'results': [{'name': 'Beach Resort', 'price': '2800', 'mock': True}]}), 200

    hotel_ids = [h['hotelId'] for h in hotels_by_city.get('data', [])[:10]]

    # Step 2: get offers for those hotels
    offers = amadeus_get('/v3/shopping/hotel-offers', {
        'hotelIds': ','.join(hotel_ids),
        'checkInDate':  check_in,
        'checkOutDate': check_out,
        'adults':       adults,
        'currencyCode': 'INR',
    })

    results = []
    if offers:
        for offer in offers.get('data', [])[:6]:
            h = offer.get('hotel', {})
            o = offer.get('offers', [{}])[0]
            results.append({
                'name':    h.get('name', 'Hotel'),
                'rating':  h.get('rating'),
                'price':   o.get('price', {}).get('total', 'N/A'),
                'room':    o.get('room', {}).get('typeEstimated', {}).get('category', 'Standard'),
            })

    return jsonify({'results': results, 'live': bool(results)})


@app.route('/api/budget/calculate', methods=['POST'])
def calculate_budget():
    data   = request.json or {}
    total  = float(data.get('total', 50000))
    days   = max(int(data.get('days', 5)), 1)
    people = max(int(data.get('people', 1)), 1)

    return jsonify({
        'stay':             round(total * 0.40),
        'food':             round(total * 0.25),
        'travel':           round(total * 0.25),
        'misc':             round(total * 0.10),
        'daily_limit':      round(total / days),
        'per_person_daily': round(total / days / people),
    })


@app.route('/health')
def health():
    has_creds = bool(AMADEUS_CLIENT_ID and AMADEUS_CLIENT_ID != 'your_api_key_here')
    token     = get_amadeus_token() if has_creds else None
    return jsonify({
        'status':        'dreamy',
        'service':       'wanderlog-api',
        'amadeus_live':  bool(token),
        'mode':          'live' if token else 'mock',
    })


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
