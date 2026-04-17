import json
import re
import os

# Load dataset
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def extract_intent(query: str):
    """
    Simple rule-based NLP to extract constraints from natural language.
    Looks for categories and price caps (e.g., 'under 2000').
    """
    query_lower = query.lower()
    
    # Extract category
    categories = ["shoes", "clothing", "electronics"]
    detected_category = None
    for cat in categories:
        if cat in query_lower:
            detected_category = cat
            break
            
    # Extract price constraint
    max_price = None
    price_match = re.search(r'(under|below|less than|max|cheaper than)\s*(?:₹|\$|rs.?|rupees)?\s*(\d+)', query_lower)
    if price_match:
        max_price = float(price_match.group(2))
        
    # Check for "cheap" or "cheaper"
    if not max_price and re.search(r'(cheap|cheaper|lowest price)', query_lower):
        # Setting a generic low cap if 'cheap' is mentioned without exact price
        max_price = 2000 
        
    return {
        "category": detected_category,
        "max_price": max_price
    }

def filter_products(query: str):
    """
    Rule-based engine: Filters based on extracted constraints and sorts by rating.
    """
    data = load_data()
    intent = extract_intent(query)
    
    # Rule 1: Must be in stock
    filtered = [item for item in data if item.get("in_stock", False)]
    
    # Rule 2: Category matching
    if intent["category"]:
        filtered = [item for item in filtered if item["category"] == intent["category"]]
        
    # Rule 3: Price constraint
    if intent["max_price"]:
        filtered = [item for item in filtered if item["price"] <= intent["max_price"]]
        
    # Rule 4: Sort by rating (descending)
    filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)
    
    # Return top 3 recommendations
    return filtered[:3], intent["category"]
