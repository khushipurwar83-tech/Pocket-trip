import json
import logging
from app.db.sqlite_db import get_sqlite_conn
from app.core.firebase import get_db

logger = logging.getLogger(__name__)

def add_to_queue(action: str, collection: str, document_id: str, data: dict):
    """
    Add write operations to local SQLite queue to be synced to Firebase later.
    """
    conn = get_sqlite_conn()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sync_queue (action, collection, document_id, data)
        VALUES (?, ?, ?, ?)
    ''', (action, collection, document_id, json.dumps(data)))
    conn.commit()
    conn.close()

def process_sync_queue():
    """
    Cron job function to process pending changes in SQLite and push them to Firestore.
    """
    db = get_db()
    if not db:
        logger.error("Firestore not available")
        return

    conn = get_sqlite_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sync_queue WHERE status = 'pending' ORDER BY timestamp ASC")
    items = cursor.fetchall()

    for item in items:
        try:
            doc_ref = db.collection(item['collection']).document(item['document_id'])
            data = json.loads(item['data'])
            
            if item['action'] == 'create' or item['action'] == 'update':
                # Last write wins by default with set(merge=True)
                doc_ref.set(data, merge=True)
            elif item['action'] == 'delete':
                doc_ref.delete()
                
            cursor.execute("UPDATE sync_queue SET status = 'completed' WHERE id = ?", (item['id'],))
        except Exception as e:
            logger.error(f"Failed to sync item {item['id']}: {e}")
            cursor.execute("UPDATE sync_queue SET retry_count = retry_count + 1 WHERE id = ?", (item['id'],))
    
    conn.commit()
    conn.close()
