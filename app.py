from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from assistant import filter_products
from llm import generate_explanation
from firebase import log_interaction, get_insights

app = FastAPI(title="Smart Retail Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    user_query = req.message
    
    # 1. Rule-based filtering logic
    recommended_items, intent = filter_products(user_query)
    
    # 2. LLM dynamic explainable response
    explanation = generate_explanation(user_query, recommended_items, intent)
    
    # 3. Log interaction to Firebase (or Mock)
    log_interaction(user_query, len(recommended_items), intent.get("category"))
    
    return {
        "explanation": explanation,
        "products": recommended_items
    }

@app.get("/insights")
def insights_endpoint():
    return get_insights()

# Make sure 'static' directory exists before mounting
os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
