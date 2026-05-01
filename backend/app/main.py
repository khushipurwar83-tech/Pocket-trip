from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from app.api.routes import budget, expenses, trips, destinations, itinerary
from app.db.sqlite_db import init_db
from app.services.offline_sync import process_sync_queue

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite db on startup
    init_db()
    
    # Start background scheduler for syncing offline data with Firebase
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_sync_queue, 'interval', minutes=5)
    scheduler.start()
    
    yield
    
    # Shutdown safely
    scheduler.shutdown()

app = FastAPI(
    title="Budget Travel Planner API", 
    description="Backend API for student budget travel planner app",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modules
app.include_router(budget.router, prefix="/api/budget", tags=["Budget"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(destinations.router, prefix="/api/destinations", tags=["Destinations"])
app.include_router(itinerary.router, prefix="/api/itinerary", tags=["Itinerary"])

@app.get("/")
def root():
    return {
        "success": True, 
        "data": {"message": "Budget Travel Planner API is running"},
        "error": None
    }
