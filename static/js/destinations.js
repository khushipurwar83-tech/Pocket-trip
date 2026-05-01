// --- wanderlog | Destinations Service ---
// Fetches from Flask backend. Falls back to built-in mock if the API is offline.

const MOCK_FALLBACK = [
    {
        id: "goa", name: "Goa", location: "India",
        lat: 15.2993, lng: 74.1240,
        image: "https://images.unsplash.com/photo-1512343879784-960f40e07e7a?w=400&h=300&fit=crop",
        heroImage: "https://images.unsplash.com/photo-1512343879784-960f40e07e7a?w=1200&h=600&fit=crop",
        description: "Sun-kissed beaches, Portuguese heritage, and vibrant nightlife",
        startPrice: 2999, vibe: "🌊 Beach vibes • Parties • Heritage", category: "beach",
        places: [
            { name: "North Goa", image: "https://images.unsplash.com/photo-1589093019248-4d6dc9f7f8f3?w=400",
              activities: ["Baga Beach", "Anjuna Flea Market", "Fort Aguada", "Saturday Night Market"] },
            { name: "South Goa", image: "https://images.unsplash.com/photo-1512100354054-b6e6f5f0f4e8?w=400",
              activities: ["Palolem Beach", "Butterfly Beach", "Colva Beach", "Dudhsagar Falls"] },
            { name: "Panaji", image: "https://images.unsplash.com/photo-1586922251167-6c9e1ee7b8b3?w=400",
              activities: ["Fontainhas", "Church of Our Lady", "Casino", "Latin Quarter"] },
        ]
    },
    {
        id: "manali", name: "Manali", location: "Himachal Pradesh",
        lat: 32.2396, lng: 77.1887,
        image: "https://images.unsplash.com/photo-1584191059421-638b2f94f471?w=400&h=300&fit=crop",
        heroImage: "https://images.unsplash.com/photo-1584191059421-638b2f94f471?w=1200&h=600&fit=crop",
        description: "Snow-capped peaks, pine forests, and adventure sports",
        startPrice: 2499, vibe: "🏔️ Mountains • Adventure • Cafes", category: "mountain",
        places: [
            { name: "Old Manali", image: "https://images.unsplash.com/photo-1626621341517-bbf1d9990a23?w=400",
              activities: ["Cafe Hopping", "River Crossing", "Hiking", "Budget Stays"] },
            { name: "Solang Valley", image: "https://images.unsplash.com/photo-1626621341517-bbf1d9990a23?w=400",
              activities: ["Paragliding", "Snow Sports", "Zorbing", "Cable Car"] },
            { name: "Rohtang Pass", image: "https://images.unsplash.com/photo-1626621341517-bbf1d9990a23?w=400",
              activities: ["Snow Activities", "Photography", "Bike Rides", "Snow Fighting"] },
        ]
    },
    {
        id: "jaipur", name: "Jaipur", location: "Rajasthan",
        lat: 26.9124, lng: 75.7873,
        image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=300&fit=crop",
        heroImage: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=1200&h=600&fit=crop",
        description: "The Pink City's royal heritage and majestic forts",
        startPrice: 3499, vibe: "🏰 Palaces • Forts • Colors", category: "heritage",
        places: [
            { name: "Amer Fort", image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400",
              activities: ["Elephant Ride", "Light Show", "Palace Tour", "Mirror Palace"] },
            { name: "City Palace", image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400",
              activities: ["Museum", "Royal Costumes", "Courtyards", "Art Gallery"] },
            { name: "Hawa Mahal", image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400",
              activities: ["Photography", "Market Shopping", "Sunset Views", "Local Food"] },
        ]
    },
    {
        id: "rishikesh", name: "Rishikesh", location: "Uttarakhand",
        lat: 30.0869, lng: 78.2676,
        image: "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400&h=300&fit=crop",
        heroImage: "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=1200&h=600&fit=crop",
        description: "Yoga capital, river rafting, and spiritual vibes",
        startPrice: 1499, vibe: "🧘 Spiritual • Rafting • Cafes", category: "spiritual",
        places: [
            { name: "Laxman Jhula", image: "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400",
              activities: ["Temples", "Cafes", "Ganga Aarti", "Shopping"] },
            { name: "Shivpuri", image: "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400",
              activities: ["River Rafting", "Camping", "Bungee Jumping", "Beach Volleyball"] },
            { name: "Triveni Ghat", image: "https://images.unsplash.com/photo-1560012057-13e6f7c5f3c4?w=400",
              activities: ["Evening Aarti", "Meditation", "Sunset", "Photography"] },
        ]
    },
    {
        id: "ladakh", name: "Ladakh", location: "J&K",
        lat: 34.1526, lng: 77.5771,
        image: "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400&h=300&fit=crop",
        heroImage: "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=1200&h=600&fit=crop",
        description: "Land of high passes — dramatic landscapes and Buddhist culture",
        startPrice: 5999, vibe: "🏍️ Adventure • Monasteries • Moonscapes", category: "adventure",
        places: [
            { name: "Pangong Lake", image: "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
              activities: ["Camping", "Star Gazing", "Photography", "Paddle Boating"] },
            { name: "Nubra Valley", image: "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
              activities: ["Double Hump Camel", "Sand Dunes", "Monasteries", "Hot Springs"] },
            { name: "Khardung La", image: "https://images.unsplash.com/photo-1587394815531-9a7b9f2f3e8b?w=400",
              activities: ["Highest Motorable Road", "Snow", "Photography", "Bike Ride"] },
        ]
    },
];

// Cache so we don't re-fetch on every navigate
window.DREAM_DESTINATIONS = null;

/**
 * Fetch destinations from backend (with live Amadeus prices when available).
 * Falls back to MOCK_FALLBACK if the API call fails.
 */
async function fetchDestinations() {
    if (window.DREAM_DESTINATIONS) return window.DREAM_DESTINATIONS;   // cached

    try {
        const res = await fetch('/api/destinations', { signal: AbortSignal.timeout(6000) });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        window.DREAM_DESTINATIONS = data;
        console.log('[wanderlog] Destinations loaded from API ✅');
    } catch (err) {
        console.warn('[wanderlog] API unavailable, using mock data:', err.message);
        window.DREAM_DESTINATIONS = MOCK_FALLBACK;
    }
    return window.DREAM_DESTINATIONS;
}

/**
 * Renders the Pinterest-style explore grid.
 */
window.loadDestinations = async function () {
    const grid = document.getElementById('trip-grid');
    if (!grid) return;

    // Skeleton shimmer while loading
    grid.innerHTML = Array(4).fill(
        `<div class="pin" style="height:320px; background: linear-gradient(90deg, var(--dream-sand) 25%, var(--dream-blush) 50%, var(--dream-sand) 75%); background-size: 400% 100%; animation: shimmer 1.4s infinite;"></div>`
    ).join('');

    const trips = await fetchDestinations();

    grid.innerHTML = '';
    trips.forEach(trip => {
        const isLive = Boolean(trip.livePrice);
        const pin = document.createElement('div');
        pin.className = 'pin';
        pin.onclick = () => window.openPlanner(trip.name);

        pin.innerHTML = `
            <div class="pin-image" style="background-image: url('${trip.image}')"></div>
            <div class="pin-info">
                <p class="caption" style="color: var(--primary);">${trip.category.toUpperCase()}</p>
                <h4 class="pin-title">${trip.name}</h4>
                <div class="pin-meta">
                    <p class="body-text" style="font-size:13px;">
                        From ₹${(trip.startPrice || trip.livePrice || 0).toLocaleString()}
                        ${isLive ? '<span style="font-size:9px;color:var(--dream-sage);font-weight:700;"> ✈ LIVE</span>' : ''}
                    </p>
                    <p class="caption" style="font-size:10px;">${trip.location}</p>
                </div>
            </div>
        `;
        grid.appendChild(pin);
    });
};

// ─── Shimmer keyframe (injected once) ────────────────────────────────────────
const style = document.createElement('style');
style.textContent = `
@keyframes shimmer {
    0%   { background-position: 100% 50%; }
    100% { background-position:   0% 50%; }
}`;
document.head.appendChild(style);
