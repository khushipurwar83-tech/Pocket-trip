import os
import time
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
CORS(app)

# ─── Amadeus Auth (optional – app works without it) ──────────────────────────

AMADEUS_CLIENT_ID     = os.environ.get('AMADEUS_CLIENT_ID', '')
AMADEUS_CLIENT_SECRET = os.environ.get('AMADEUS_CLIENT_SECRET', '')
AMADEUS_BASE          = 'https://test.api.amadeus.com'

_token_cache = {'token': None, 'expires_at': 0}

def get_amadeus_token():
    if _token_cache['token'] and time.time() < _token_cache['expires_at']:
        return _token_cache['token']
    if not AMADEUS_CLIENT_ID or AMADEUS_CLIENT_ID in ('', 'your_api_key_here'):
        return None
    try:
        r = requests.post(
            f'{AMADEUS_BASE}/v1/security/oauth2/token',
            data={'grant_type': 'client_credentials',
                  'client_id': AMADEUS_CLIENT_ID,
                  'client_secret': AMADEUS_CLIENT_SECRET},
            timeout=8
        )
        r.raise_for_status()
        d = r.json()
        _token_cache['token']      = d['access_token']
        _token_cache['expires_at'] = time.time() + d['expires_in'] - 60
        return _token_cache['token']
    except Exception as e:
        print(f'[Amadeus] Token error: {e}')
        return None

def amadeus_get(path, params=None):
    token = get_amadeus_token()
    if not token:
        return None
    try:
        r = requests.get(f'{AMADEUS_BASE}{path}',
                         headers={'Authorization': f'Bearer {token}'},
                         params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f'[Amadeus] {path} error: {e}')
        return None

# ─── Open-Meteo: free weather, no key needed ─────────────────────────────────

def get_weather(lat, lng):
    """Fetch current temperature for a location — free, no API key."""
    try:
        r = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={'latitude': lat, 'longitude': lng,
                    'current_weather': 'true', 'forecast_days': 1},
            timeout=5
        )
        r.raise_for_status()
        cw = r.json().get('current_weather', {})
        return {
            'temp_c':    cw.get('temperature'),
            'wind_kmh':  cw.get('windspeed'),
            'is_day':    cw.get('is_day', 1),
        }
    except Exception:
        return None

# ─── Curated destination catalog ─────────────────────────────────────────────

DESTINATIONS = [
    {
        "id": "goa",          "name": "Goa",
        "location": "India",  "lat": 15.2993, "lng": 74.1240,
        "image":     "https://images.unsplash.com/photo-1512343879784-960f40e07e7a?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1512343879784-960f40e07e7a?w=1200&h=600&fit=crop",
        "description": "Sun-kissed beaches, Portuguese heritage, and vibrant nightlife",
        "startPrice": 2999, "vibe": "Beach vibes • Parties • Heritage",
        "category": "beach", "iataCode": "GOI",
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
        "startPrice": 2499, "vibe": "Mountains • Adventure • Cafes",
        "category": "mountain", "iataCode": "KUU",
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
        "startPrice": 3499, "vibe": "Palaces • Forts • Colors",
        "category": "heritage", "iataCode": "JAI",
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
        "startPrice": 1499, "vibe": "Spiritual • Rafting • Cafes",
        "category": "spiritual", "iataCode": "DED",
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
        "startPrice": 5999, "vibe": "Adventure • Monasteries • Moonscapes",
        "category": "adventure", "iataCode": "IXL",
        "places": [
            {"name": "Pangong Lake", "image": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
             "activities": ["Camping", "Star Gazing", "Photography", "Paddle Boating"]},
            {"name": "Nubra Valley", "image": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
             "activities": ["Double Hump Camel", "Sand Dunes", "Monasteries", "Hot Springs"]},
            {"name": "Khardung La",  "image": "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
             "activities": ["Highest Motorable Road", "Snow", "Photography", "Bike Ride"]},
        ]
    },
    {
        "id": "wayanad",      "name": "Wayanad",
        "location": "Kerala", "lat": 11.6854, "lng": 76.1111,
        "image":     "https://images.unsplash.com/photo-1589043758552-0c0df3d7c9c1?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1589043758552-0c0df3d7c9c1?w=1200&h=600&fit=crop",
        "description": "Green tea plantations, waterfalls, and wildlife",
        "startPrice": 2799, "vibe": "Nature • Trekking • Wildlife",
        "category": "mountain", "iataCode": "CCJ",
        "places": [
            {"name": "Chembra Peak", "image": "https://images.unsplash.com/photo-1589043758552-0c0df3d7c9c1?w=400",
             "activities": ["Trekking", "Heart Shaped Lake", "Sunrise Views", "Photography"]},
            {"name": "Edakkal Caves","image": "https://images.unsplash.com/photo-1589043758552-0c0df3d7c9c1?w=400",
             "activities": ["History", "Ancient Carvings", "Trek", "Archaeology"]},
            {"name": "Banasura Dam", "image": "https://images.unsplash.com/photo-1589043758552-0c0df3d7c9c1?w=400",
             "activities": ["Boating", "Picnic", "Sunset", "Nature Walk"]},
        ]
    },
    {
        "id": "coorg",        "name": "Coorg",
        "location": "Karnataka", "lat": 12.3375, "lng": 75.8069,
        "image":     "https://images.unsplash.com/photo-1583228946846-ebd8c1b9f4f6?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1583228946846-ebd8c1b9f4f6?w=1200&h=600&fit=crop",
        "description": "Scotland of India — coffee estates and misty hills",
        "startPrice": 2999, "vibe": "Coffee • Mist • Waterfalls",
        "category": "mountain", "iataCode": "MYQ",
        "places": [
            {"name": "Abbey Falls",  "image": "https://images.unsplash.com/photo-1583228946846-ebd8c1b9f4f6?w=400",
             "activities": ["Waterfall View", "Photography", "Nature Walk", "Picnic"]},
            {"name": "Raja's Seat",  "image": "https://images.unsplash.com/photo-1583228946846-ebd8c1b9f4f6?w=400",
             "activities": ["Sunset Views", "Gardens", "Toy Train", "Musical Fountain"]},
            {"name": "Dubare Camp",  "image": "https://images.unsplash.com/photo-1583228946846-ebd8c1b9f4f6?w=400",
             "activities": ["Elephant Bath", "River Rafting", "Camping", "Nature Trail"]},
        ]
    },
    {
        "id": "pondicherry",  "name": "Pondicherry",
        "location": "Tamil Nadu", "lat": 11.9141, "lng": 79.8145,
        "image":     "https://images.unsplash.com/photo-1582285409513-24fc958cb605?w=400&h=300&fit=crop",
        "heroImage": "https://images.unsplash.com/photo-1582285409513-24fc958cb605?w=1200&h=600&fit=crop",
        "description": "French colonial charm by the Bay of Bengal",
        "startPrice": 1999, "vibe": "French quarters • Serene beaches • Spiritual",
        "category": "heritage", "iataCode": "PNY",
        "places": [
            {"name": "French Quarter","image": "https://images.unsplash.com/photo-1582285409513-24fc958cb605?w=400",
             "activities": ["Promenade Beach", "Sri Aurobindo Ashram", "French Cafes", "Boutique Shopping"]},
            {"name": "Auroville",    "image": "https://images.unsplash.com/photo-1582285409513-24fc958cb605?w=400",
             "activities": ["Matrimandir", "Buddha Garden", "Workshops", "Meditation"]},
            {"name": "Paradise Beach","image": "https://images.unsplash.com/photo-1582285409513-24fc958cb605?w=400",
             "activities": ["Boating", "Sunset Views", "Water Sports", "Beach Walking"]},
        ]
    },
]

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/destinations')
def get_destinations():
    """
    Returns curated destinations enriched with:
    - Live weather (Open-Meteo, always free, no key needed)
    - Live flight prices (Amadeus, only when keys are configured)
    """
    results = []
    has_amadeus = bool(get_amadeus_token())

    for dest in DESTINATIONS:
        item = dest.copy()

        # --- Real weather (always works) ---
        weather = get_weather(dest['lat'], dest['lng'])
        if weather:
            item['weather'] = weather

        # --- Live flight prices (Amadeus, optional) ---
        if has_amadeus:
            flight_data = amadeus_get('/v1/shopping/flight-destinations', {
                'origin':      'DEL',
                'destination': dest.get('iataCode', ''),
                'maxPrice':    20000,
            })
            if flight_data and flight_data.get('data'):
                price = flight_data['data'][0].get('price', {}).get('total')
                if price:
                    item['livePrice']   = float(price)
                    item['startPrice']  = int(float(price))

        results.append(item)

    return jsonify(results)


@app.route('/api/flights/search')
def search_flights():
    origin      = request.args.get('origin', 'DEL').upper()
    destination = request.args.get('destination', 'GOI').upper()
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
        # Friendly mock fallback so UI always shows something
        return jsonify({'live': False, 'results': [
            {'price': '3,499', 'currency': 'INR',
             'segments': [{'departure': origin, 'arrival': destination,
                           'departureAt': f'{date}T06:00', 'arrivalAt': f'{date}T08:30',
                           'carrier': 'IndiGo', 'duration': 'PT2H30M'}]},
            {'price': '4,299', 'currency': 'INR',
             'segments': [{'departure': origin, 'arrival': destination,
                           'departureAt': f'{date}T14:00', 'arrivalAt': f'{date}T16:45',
                           'carrier': 'Air India', 'duration': 'PT2H45M'}]},
        ]})

    results = []
    for offer in data.get('data', []):
        results.append({
            'price':    offer['price']['grandTotal'],
            'currency': offer['price']['currency'],
            'segments': [
                {'departure':   seg['departure']['iataCode'],
                 'arrival':     seg['arrival']['iataCode'],
                 'departureAt': seg['departure']['at'],
                 'arrivalAt':   seg['arrival']['at'],
                 'carrier':     seg.get('carrierCode', ''),
                 'duration':    seg.get('duration', '')}
                for itin in offer['itineraries']
                for seg in itin['segments']
            ]
        })
    return jsonify({'live': True, 'results': results})


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
    token = get_amadeus_token()
    return jsonify({
        'status':       'dreamy',
        'service':      'wanderlog-api',
        'amadeus_live': bool(token),
        'weather_live': True,   # Open-Meteo always works
        'mode':         'live' if token else 'weather+mock',
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
