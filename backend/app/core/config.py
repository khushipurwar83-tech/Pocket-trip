import os

class Settings:
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-adminsdk.json")
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "sync_queue.db")

settings = Settings()
