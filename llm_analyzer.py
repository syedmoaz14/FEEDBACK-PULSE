# llm_analyzer.py

import os
import json
from google import genai
from google.genai.errors import APIError

# --- P3.1: Define the Structured Output Schema ---
ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "string",
            "description": "The overall emotional tone. Must be one of: Positive, Negative, or Neutral."
        },
        "topic": {
            "type": "string",
            "description": "A single, high-level business topic the review addresses. Choose from: Sizing_Fit, Quality, Shipping_Delivery, Price_Value, Customer_Service, Design_Style."
        },
        "action_item": {
            "type": "string",
            "description": "A short, actionable suggestion for the business based ONLY on this review (e.g., 'Increase stock of XXL size,' 'Improve clarity of return policy')."
        }
    },
    "required": ["sentiment", "topic", "action_item"]
}

# --- P2.3: Initialize Client (Robustly handles key lookup) ---
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("FATAL ERROR in llm_analyzer: GEMINI_API_KEY environment variable not found.")
    client = None
else:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        client = None


def call_llm_analysis(review_text: str) -> dict:
    """
    Sends a single review to the LLM for structured analysis.
    """
    if client is None:
        return None

    # P3.2: Prompt Engineering (The Rules)
    system_instruction = (
        "You are an expert customer feedback analyst for an e-commerce fashion retailer. "
        "Your task is to analyze a single customer review and extract three key insights "
        "in the requested JSON format. Strictly adhere to the output format."
        "Allowed topics are: Sizing_Fit, Quality, Shipping_Delivery, Price_Value, Customer_Service, Design_Style."
    )

    user_prompt = f"Analyze the following customer review and provide the required structured JSON analysis: \n\n'{review_text}'"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ANALYSIS_SCHEMA
            )
        )
        return json.loads(response.text)

    except Exception as e:
        print(f"Error analyzing review: {e}. Review text: {review_text[:50]}...")
        return None