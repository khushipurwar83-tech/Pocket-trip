// --- wanderlog | dream it, plan it ---
console.log('wanderlog initialized...');

// --- Global App State ---
const AppState = {
    isLoggedIn: false,
    user: null,
    setup: { budget: 50000, days: 5 },
    currentTrip: {
        id: 1,
        name: 'Goa, India',
        totalBudget: 50000,
        days: 5,
        spent: 0,
        active: true
    },
    savedDreams: [
        { id: 1, name: 'Santorini', image: 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=400&h=600&auto=format&fit=crop' },
        { id: 2, name: 'Tokyo', image: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=400&h=500&auto=format&fit=crop' },
        { id: 3, name: 'Swiss Alps', image: 'https://images.unsplash.com/photo-1531310197839-ccf54634509e?q=80&w=400&h=600&auto=format&fit=crop' }
    ],
    expenses: [
        { id: 1, desc: 'Beachfront Dinner', amount: 2500, category: 'Dining', date: 'Today, 8:00 PM', icon: '🍷' },
        { id: 2, desc: 'Surfing Lesson', amount: 1500, category: 'Experience', date: 'Yesterday', icon: '🏄' }
    ]
};

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    
    // Global delegation for onboarding setup
    document.addEventListener('click', (e) => {
        const durationBtn = e.target.closest('.duration-btn');
        if(durationBtn) {
            document.querySelectorAll('.duration-btn').forEach(b => b.classList.remove('active'));
            durationBtn.classList.add('active');
            AppState.setup.days = parseInt(durationBtn.getAttribute('data-days'));
        }
    });
});

function initApp() {
    loadState();
    setupNavigation();
    
    if (AppState.isLoggedIn) {
        showScreen('home');
        updateDashboard();
    } else {
        showScreen('login');
    }
}

// --- Navigation ---
function setupNavigation() {
    window.navigate = showScreen;
}

function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(el => {
        el.classList.remove('active');
        el.classList.add('hidden');
    });
    
    // Handle bottom nav visibility
    const nav = document.getElementById('bottom-nav');
    if (screenId === 'login' || screenId === 'onboarding') {
        if(nav) nav.classList.add('hidden');
    } else {
        if(nav) nav.classList.remove('hidden');
    }

    const target = document.getElementById(screenId);
    if(target) {
        target.classList.remove('hidden');
        target.classList.add('active');
    }
    
    // Update active nav item
    if (nav && !nav.classList.contains('hidden')) {
        document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
        const navMap = { 'home': 0, 'discover': 1, 'screen-map': 2, 'budget': 3, 'profile': 4 };
        const index = navMap[screenId];
        if (index !== undefined) {
            document.querySelectorAll('.nav-item')[index].classList.add('active');
        }
    }

    // Screen specific logic
    if (screenId === 'screen-map' && window.initMap) {
        setTimeout(() => window.initMap(), 100);
    } else if (screenId === 'budget' && typeof window.initChart === 'function') {
        setTimeout(() => window.initChart(), 50);
    } else if (screenId === 'discover') {
        window.loadDestinations();
    } else if (screenId === 'home') {
        updateDashboard();
    } else if (screenId === 'active-trip') {
        renderActiveTripPage();
    }
}

// --- Auth ---
window.handleLogin = function() {
    const loader = document.getElementById('global-loader');
    if(loader) loader.classList.remove('hidden');
    
    setTimeout(() => {
        AppState.isLoggedIn = true;
        AppState.user = { name: 'Alex' };
        saveState();
        if(loader) loader.classList.add('hidden');
        showScreen('home');
    }, 1500);
};

// --- Core Actions ---
window.handleStartPlanning = function() {
    const budgetVal = document.getElementById('budgetInput').value;
    const finalBudget = budgetVal ? parseInt(budgetVal) : AppState.setup.budget;
    startJourney(finalBudget, AppState.setup.days);
};

window.startJourney = function(budget, days) {
    const loader = document.getElementById('global-loader');
    if(loader) loader.classList.remove('hidden');
    
    AppState.currentTrip.totalBudget = budget;
    AppState.currentTrip.days = days;
    AppState.expenses = []; // Reset for new trip
    
    saveState();

    setTimeout(() => {
        if(loader) loader.classList.add('hidden');
        showScreen('home');
        updateDashboard();
    }, 1200);
};

window.openPlanner = function(name) {
    document.getElementById('plan-dest-name').innerText = name;
    document.getElementById('planner-modal').classList.remove('hidden');
};

window.createTripFromPin = function() {
    const budget = parseInt(document.getElementById('planBudget').value) || 50000;
    const days = parseInt(document.getElementById('planDays').value) || 5;
    const name = document.getElementById('plan-dest-name').innerText;
    
    AppState.currentTrip.name = name;
    document.getElementById('planner-modal').classList.add('hidden');
    startJourney(budget, days);
};

function updateDashboard() {
    if(!AppState.isLoggedIn) return;
    
    // Update Stats
    document.getElementById('userName').innerText = AppState.user.name || 'Dreamer';
    document.getElementById('tripCount').innerText = '8'; // Mock stat
    document.getElementById('savedCount').innerText = AppState.savedDreams.length;
    
    // Active Trip Section
    const activeSection = document.getElementById('activeTripSection');
    if (AppState.currentTrip && AppState.currentTrip.active) {
        activeSection.style.display = 'block';
        renderActiveTripCard();
    } else {
        activeSection.style.display = 'none';
    }
    
    renderSavedDreams();
}

function renderActiveTripCard() {
    const container = document.getElementById('activeTripCard');
    const trip = AppState.currentTrip;
    const spent = AppState.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const left = trip.totalBudget - spent;
    const pct = Math.min((spent / trip.totalBudget) * 100, 100);

    container.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
            <div>
                <h3 class="headline-small">${trip.name}</h3>
                <p class="body-text">${trip.days || 5} days exploration</p>
            </div>
            <div style="text-align: right;">
                <p class="caption">REMAINING</p>
                <p class="headline-small" style="color: var(--primary-warm);">₹${left.toLocaleString()}</p>
            </div>
        </div>
        <div class="progress-container" style="margin-bottom: 12px;">
            <div class="progress-bar" style="width: ${pct}%"></div>
        </div>
        <p class="caption">${Math.round(pct)}% of dream budget used</p>
        <button class="btn btn-outline w-100 mt-4" onclick="navigate('active-trip')">View Journey Details →</button>
    `;
}

function renderActiveTripPage() {
    const trip = AppState.currentTrip;
    if(!trip) return;
    
    // Find destination data
    const destData = (window.DREAM_DESTINATIONS || []).find(d => d.name === trip.name) || window.DREAM_DESTINATIONS[0];
    
    document.getElementById('tripTitle').innerText = trip.name;
    const hero = document.getElementById('tripHero');
    if(hero) hero.style.backgroundImage = `url('${destData.heroImage || destData.image}')`;
    
    const spent = AppState.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const left = trip.totalBudget - spent;
    
    document.getElementById('tripBudget').innerText = `₹${trip.totalBudget.toLocaleString()}`;
    document.getElementById('tripSpent').innerText = `₹${spent.toLocaleString()}`;
    document.getElementById('tripRemaining').innerText = `₹${left.toLocaleString()}`;
    
    // Render Itinerary
    const itineraryList = document.getElementById('dailyItinerary');
    if(itineraryList) {
        itineraryList.innerHTML = destData.places.map((place, idx) => `
            <div class="card" style="padding: 16px; background: white;">
                <div style="display: flex; gap: 16px; align-items: center;">
                    <div style="width: 60px; height: 60px; border-radius: 12px; background-image: url('${place.image}'); background-size: cover;"></div>
                    <div>
                        <h4 style="font-family: 'Playfair Display', serif; font-size: 18px;">${place.name}</h4>
                        <p class="caption">DAY 0${idx + 1}</p>
                    </div>
                </div>
                <div style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px;">
                    ${place.activities.map(a => `<span class="pin-vibe" style="font-size: 10px;">${a}</span>`).join('')}
                </div>
            </div>
        `).join('');
    }
    
    // Render Expenses
    const expList = document.getElementById('expensesList');
    if(expList) {
        expList.innerHTML = AppState.expenses.map(exp => `
            <div class="transaction-item" style="background: white; margin-bottom: 12px;">
                <div class="transaction-icon">${exp.icon || '📍'}</div>
                <div class="transaction-details">
                    <div class="transaction-name">${exp.desc}</div>
                    <div class="transaction-date">${exp.date}</div>
                </div>
                <div class="transaction-amount">-₹${exp.amount}</div>
            </div>
        `).join('');
    }
}

window.endCurrentTrip = function() {
    if(confirm('Are you ready to conclude this journey? It will be saved to your past memories.')) {
        AppState.currentTrip.active = false;
        saveState();
        navigate('home');
    }
};

window.goToActiveTrip = function() {
    navigate('active-trip');
};

window.showMapPage = function() {
    navigate('screen-map');
};

// --- Persistence Bridge ---
function saveState() {
    window.saveState(AppState);
}

function loadState() {
    const saved = window.loadState();
    if (saved) {
        Object.assign(AppState, saved);
    }
}

window.clearCache = function() {
    if(confirm('Delete your dream board?')) {
        localStorage.removeItem('wanderlog_state');
        location.reload();
    }
};
