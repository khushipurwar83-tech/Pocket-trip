import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from app.core.config import settings

def get_db():
    if not firebase_admin._apps:
        try:
            # Check if we should load from ENV var (e.g. on Render)
            if os.getenv("FIREBASE_CREDENTIALS_JSON"):
                cred_dict = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))
                cred = credentials.Certificate(cred_dict)
            else:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Failed to initialize Firebase (Warning): {e}")
            pass
    try:
        db = firestore.client()
        return db
    except:
        return None
