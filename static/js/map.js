// --- wanderlog | Dream Map Board ---

let map;
let markers;

const createDreamPin = (destination) => {
    return L.divIcon({
        className: 'dream-pin-marker',
        html: `
            <div class="pin-card">
                <div class="pin-image" style="background-image: url('${destination.image}')">
                    <div class="pin-overlay"></div>
                    <div class="pin-price">✨ From ₹${destination.startPrice}</div>
                </div>
                <div class="pin-info">
                    <div class="pin-title">${destination.name}</div>
                    <div class="pin-location">📍 ${destination.location}</div>
                    <div class="pin-vibe" style="font-size: 8px;">${destination.vibe.split('•')[0]}</div>
                </div>
            </div>
        `,
        iconSize: [180, 220],
        iconAnchor: [90, 220],
        popupAnchor: [0, -220]
    });
};

window.initMap = function() {
    if (map) {
        setTimeout(() => map.invalidateSize(), 100);
        return;
    }

    // Default view centered on India
    map = L.map('dreamMap', { zoomControl: false }).setView([20.5937, 78.9629], 5);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    renderGems();
    L.control.zoom({ position: 'bottomright' }).addTo(map);
};

function renderGems() {
    if (markers) map.removeLayer(markers);
    markers = L.layerGroup();

    const destinations = window.DREAM_DESTINATIONS || [];

    destinations.forEach(dest => {
        const marker = L.marker([dest.lat, dest.lng], {
            icon: createDreamPin(dest)
        });

        const popupContent = `
            <div style="color: #3D352E; font-family: 'Outfit', sans-serif; padding: 12px; min-width: 200px;">
                <p class="caption" style="margin-bottom: 4px; color: #D4A373;">${dest.category.toUpperCase()}</p>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; margin-bottom: 8px;">${dest.name}</h3>
                <p style="font-size: 13px; color: #7A6F63; margin-bottom: 12px;">${dest.vibe}</p>
                <div style="font-size: 12px; line-height: 1.5; color: #7A6F63; background: #F5F1E9; padding: 12px; border-radius: 16px; margin-bottom: 20px;">
                    ${dest.description}
                </div>
                <button class="btn btn-primary" style="width: 100%; padding: 12px; font-size: 14px;" onclick="openPlanner('${dest.name}')">Plan This Dream</button>
            </div>
        `;

        marker.bindPopup(popupContent, {
            className: 'dream-map-popup',
            maxWidth: 260
        });

        markers.addLayer(marker);
    });

    markers.addTo(map);
}
