import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase conditionally
db = None
try:
    # Attempt to initialize with credentials if provided
    cred = credentials.Certificate("firebase-credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase initialized successfully.")
except Exception as e:
    logger.warning(f"Firebase initialization skipped or failed: {e}. Running with mock logging.")
    db = None

# Mock in-memory storage for insights if firebase config is missing
mock_logs = []

def log_interaction(user_query: str, recommendation_count: int, category_detected: str):
    """
    Logs user interactions to Firestore, or to memory if Firestore is unavailable.
    """
    log_data = {
        "query": user_query,
        "recommendation_count": recommendation_count,
        "category": category_detected,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    }
    
    if db:
        try:
            db.collection("interactions").add(log_data)
        except Exception as e:
            logger.error(f"Failed to log to Firebase: {e}")
            mock_logs.append(log_data)
    else:
        mock_logs.append(log_data)

def get_insights():
    """
    Calculates basic insights from logged data.
    """
    if db:
        try:
            interactions = db.collection("interactions").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(100).stream()
            logs = [doc.to_dict() for doc in interactions]
        except Exception:
            logs = mock_logs
    else:
        logs = mock_logs

    if not logs:
        return {
            "total_queries": 0,
            "most_searched_category": "N/A",
            "recent_queries": []
        }
    
    categories = [log.get("category") for log in logs if log.get("category")]
    most_searched_category = max(set(categories), key=categories.count) if categories else "N/A"
    
    return {
        "total_queries": len(logs),
        "most_searched_category": most_searched_category,
        "recent_queries": [log.get("query") for log in logs[:5]]
    }
