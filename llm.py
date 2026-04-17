import os
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

def configure_llm():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment variables. LLM capabilities will drop to fallback mode.")
        return False
    
    genai.configure(api_key=api_key)
    return True

def generate_explanation(user_query: str, recommended_items: list) -> str:
    """
    Uses Gemini to format the response and provide explainable AI reasoning.
    The filtering happens logically in assistant.py, the LLM just explains *why*.
    """
    if not configure_llm():
        # Fallback explanation if no API key
        if not recommended_items:
            return "I couldn't find any products matching your criteria that are currently in stock."
        names = ", ".join([item['name'] for item in recommended_items])
        return f"Based on your query, here are some top recommendations: {names}. These meet your criteria and are highly rated by our customers."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        items_description = "\n".join([
            f"- {item['name']} (Price: ₹{item['price']}, Rating: {item['rating']}): {item['description']}"
            for item in recommended_items
        ])
        
        prompt = f"""
        You are a highly helpful and polite AI shopping assistant.
        The user asked: "{user_query}"
        
        The rule-based engine has selected the following products to recommend:
        {items_description if recommended_items else "None found."}
        
        Generate a concise, friendly response explaining *why* these specific items were recommended to the user based on their query constraints (like budget, category).
        Do not mention the "rule-based engine" or internal logic. Act naturally. Keep the response under 3 sentences.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}")
        return "I found some great options for you based on your needs! Please check them out below."
