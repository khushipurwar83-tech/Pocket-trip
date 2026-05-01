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
    setupNavigation();
    // Firebase auth is now handled in the HTML initialization
}

function setAppUser(user) {
    AppState.user = {
        uid: user.uid,
        email: user.email || '',
        name: user.displayName || (user.email ? user.email.split('@')[0] : 'Dreamer'),
        photoURL: user.photoURL || ''
    };
}

function getStorageKey(uid) {
    return uid ? `wanderlog_state_${uid}` : 'wanderlog_state';
}

function loadStateForUser(uid) {
    const key = getStorageKey(uid);
    const saved = window.loadState(key) || window.loadState('wanderlog_state');
    if (saved) {
        Object.assign(AppState, saved);
    }
}

function showAuthError(message) {
    const errorEl = document.getElementById('loginError');
    if (!errorEl) return;
    if (!message) {
        errorEl.textContent = '';
        errorEl.classList.add('hidden');
        errorEl.classList.remove('visible');
        return;
    }
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
    errorEl.classList.add('visible');
}

window.handleLogin = async function() {
    const loader = document.getElementById('global-loader');
    const email = document.getElementById('loginEmail')?.value.trim();
    const password = document.getElementById('loginPassword')?.value.trim();

    if (!email || !password) {
        showAuthError('Please enter both email and password.');
        return;
    }

    if (loader) loader.classList.remove('hidden');
    showAuthError('');

    try {
        await firebaseAuth.signInWithEmailAndPassword(email, password);
    } catch (error) {
        showAuthError(error.message || 'Unable to sign in.');
    } finally {
        if (loader) loader.classList.add('hidden');
    }
};

window.handleSignUp = async function() {
    const loader = document.getElementById('global-loader');
    const email = document.getElementById('loginEmail')?.value.trim();
    const password = document.getElementById('loginPassword')?.value.trim();

    if (!email || !password) {
        showAuthError('Please enter email and password to create an account.');
        return;
    }

    if (loader) loader.classList.remove('hidden');
    showAuthError('');

    try {
        await firebaseAuth.createUserWithEmailAndPassword(email, password);
    } catch (error) {
        showAuthError(error.message || 'Unable to create account.');
    } finally {
        if (loader) loader.classList.add('hidden');
    }
};

window.handleGoogleLogin = async function() {
    const loader = document.getElementById('global-loader');
    if (loader) loader.classList.remove('hidden');
    showAuthError('');

    try {
        await firebaseAuth.signInWithRedirect(window.firebaseGoogleProvider);
    } catch (error) {
        showAuthError(error.message || 'Unable to sign in with Google.');
        if (loader) loader.classList.add('hidden');
    }
};

window.logoutUser = async function() {
    if (!window.firebaseAuth) return;
    try {
        await firebaseAuth.signOut();
    } finally {
        AppState.isLoggedIn = false;
        AppState.user = null;
        showScreen('login');
    }
};

function updateProfileUI() {
    const nameEl = document.getElementById('profileName');
    const emailEl = document.getElementById('profileEmail');
    const avatarEl = document.getElementById('profileAvatar');
    if (AppState.user) {
        if (nameEl) nameEl.innerText = AppState.user.name || 'Dreamer';
        if (emailEl) emailEl.innerText = AppState.user.email || 'Welcome aboard';
        if (avatarEl) avatarEl.innerText = AppState.user.name ? AppState.user.name.charAt(0).toUpperCase() : 'W';
    }
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

// --- Flight Search ---
window.searchFlights = async function () {
    const origin  = (document.getElementById('flightOrigin')?.value || 'DEL').toUpperCase();
    const date    = document.getElementById('flightDate')?.value || '2025-06-01';
    const results = document.getElementById('flightResults');
    if (!results) return;

    // Derive IATA code from current trip destination
    const destData = (window.DREAM_DESTINATIONS || []).find(d => d.name === AppState.currentTrip?.name);
    const iata = destData?.iataCode || 'GOI';

    results.innerHTML = `<div class="body-text" style="padding:20px;text-align:center;">Searching for flights ✈️ ...</div>`;

    try {
        const res  = await fetch(`/api/flights/search?origin=${origin}&destination=${iata}&date=${date}&adults=1`);
        const data = await res.json();

        if (!data.results || data.results.length === 0) {
            results.innerHTML = `<p class="body-text" style="text-align:center;padding:20px;">No flights found for this route.</p>`;
            return;
        }

        const badge = data.live
            ? `<span style="font-size:9px;color:var(--dream-sage);font-weight:700;"> ✈ LIVE PRICES</span>`
            : `<span style="font-size:9px;color:var(--text-light);font-weight:700;"> (Sample prices)</span>`;

        results.innerHTML = data.results.map(f => `
            <div class="card" style="background:white;padding:16px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <p class="headline-small" style="font-size:20px;color:var(--primary);">
                            ₹${parseFloat(f.price).toLocaleString()} ${badge}
                        </p>
                        ${(f.segments || []).map(s => `
                            <p class="body-text" style="font-size:12px;margin-top:4px;">
                                ${s.departure} → ${s.arrival} &nbsp;|&nbsp; ${s.departureAt?.slice(11,16) || '--'} – ${s.arrivalAt?.slice(11,16) || '--'}
                                ${s.carrier ? `&nbsp;|&nbsp; ${s.carrier}` : ''}
                            </p>
                        `).join('')}
                    </div>
                    <button class="btn btn-primary" style="padding:10px 16px;font-size:12px;">Book</button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        results.innerHTML = `<p class="body-text" style="color:var(--dream-rose);text-align:center;">Couldn't fetch flights. Try again.</p>`;
        console.error('[wanderlog] Flight search error:', err);
    }
};

// --- Persistence Bridge ---
function saveState() {
    const key = getStorageKey(AppState.user?.uid);
    window.saveState(AppState, key);
}

function loadState() {
    if (!AppState.user?.uid) return;
    const key = getStorageKey(AppState.user.uid);
    const saved = window.loadState(key) || window.loadState('wanderlog_state');
    if (saved) {
        Object.assign(AppState, saved);
    }
}

window.clearCache = function() {
    const key = getStorageKey(AppState.user?.uid);
    window.clearState(key);
};
