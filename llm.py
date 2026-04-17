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

def generate_explanation(user_query: str, recommended_items: list, intent: dict) -> str:
    """
    Uses Gemini to format the response and provide explainable AI reasoning.
    The filtering happens logically in assistant.py, the LLM just explains *why*.
    """
    budget_info = intent.get("max_price")
    budget_str = f"under ₹{budget_info}" if budget_info else "within your budget"

    if not configure_llm():
        # Fallback explanation if no API key
        if not recommended_items:
            return "I couldn't find any products matching your criteria that are currently in stock."
        
        explanations = []
        for item in recommended_items:
            price_str = f"under ₹{budget_info}" if budget_info else f"priced at ₹{item['price']}"
            explanations.append(f"I recommend {item['name']} because it is {price_str}, highly rated, and matches your requirement.")
        
        return "\n\n".join(explanations)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        items_description = "\n".join([
            f"- {item['name']} (Price: ₹{item['price']}, Rating: {item['rating']}, Category: {item['category']})"
            for item in recommended_items
        ])
        
        prompt = f"""
        You are a highly helpful and polite AI shopping assistant.
        The user asked: "{user_query}"
        
        The selected products are:
        {items_description if recommended_items else "None found."}
        
        Generate a concise, friendly response.
        For EACH recommended product, you MUST include an explainable reason.
        You MUST strictly use this exact phrasing format for each item:
        "I recommend [product] because it is {budget_str} (or 'priced at ₹[price]' if no budget was specified), highly rated, and matches your requirement."
        
        Example:
        I recommend Nike Air Max because it is under ₹5000, highly rated, and matches your requirement.
        
        Do not mention the internal logic or rules. Just provide the formatted recommendations to the user.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}")
        return "I found some great options for you based on your needs! Please check them out below."
