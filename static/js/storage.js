// --- wanderlog | LocalStorage Management ---

window.saveState = function(state, key = 'wanderlog_state') {
    try {
        localStorage.setItem(key, JSON.stringify(state));
    } catch (err) {
        console.error('Unable to save state:', err);
    }
};

window.loadState = function(key = 'wanderlog_state') {
    try {
        const saved = localStorage.getItem(key);
        if (saved) {
            return JSON.parse(saved);
        }
    } catch (err) {
        console.error('Unable to load state:', err);
    }
    return null;
};

window.clearState = function(key = 'wanderlog_state') {
    if (confirm('Delete your dream board? This will remove only your local Wanderlog data.')) {
        localStorage.removeItem(key);
        window.location.reload();
    }
};
