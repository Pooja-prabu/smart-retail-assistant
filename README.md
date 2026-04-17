# Smart Retail Assistant

A lightweight AI-powered chat assistant for retail recommendations built with **FastAPI**, **Pure JS/HTML/CSS**, and **Google Gemini**.

## Features
- **AI Chatbot**: Contextual responses dynamically formatted using the Gemini LLM.
- **Rule-Based Engine**: Safe logic ensuring correct filtering by price, category, and limits to keep business rules strictly decoupled from hallucinative API generations.
- **Explainable AI**: The LLM analyzes the dataset filtered by the rule engine to generate reason-oriented explanations.
- **Minimalist Web UI**: Responsive, glassmorphic design in a single HTML file.
- **Insights Dashboard**: Built-in `/insights` endpoint and UI button for basic session analytics.
- **Firebase Ready**: Connects automatically to Firebase Firestore interaction logging (defaults gracefully to in-memory mocks if not configured).

## File Structure
- `app.py`: FastAPI server setup and routes.
- `assistant.py`: Rule-based NLP and dataset filtering logic.
- `llm.py`: Google Gemini API wrapper for response generation.
- `firebase.py`: Logging integrations.
- `data.json`: Static, lightweight database.
- `static/index.html`: The user interface.

## Getting Started

### 1. Requirements Setup
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
To get the most out of the system, set your valid Gemini API Key:
```bash
# Windows
set GEMINI_API_KEY=your_api_key

# Linux/Mac
export GEMINI_API_KEY="your_api_key"
```

*(Optional)* If you want full Firebase usage, place a `firebase-credentials.json` at the root!

### 3. Run the App
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000/` in your browser.
