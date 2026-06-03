import os
from google import genai
from PIL import Image

# Initialize the client using the environment variable
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_screenshot(image_path: str) -> dict:
    try:
        # Load the image using Pillow
        img = Image.open(image_path)
        
        # Use the latest Google GenAI SDK method
        # Using gemini-1.5-flash as it is highly efficient for vision tasks 
        # and has a generous free tier.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Analyze this IT error screenshot. Extract the visible error text, identify the issue, and provide a numbered list of fixes.",
                img
            ]
        )
        
        ai_text = response.text
        
        # Structure the response
        return {
            "extracted_text": "Extracted by Gemini",
            "detected_errors": ["Analyzed successfully"],
            "suggested_fix": ai_text,
            "confidence": "High"
        }
        
    except Exception as e:
        # Debugging output to your terminal
        print(f"DEBUG: Gemini SDK Error: {str(e)}")
        return {
            "extracted_text": "Error",
            "detected_errors": [str(e)],
            "suggested_fix": "Failed to communicate with Gemini AI.",
            "confidence": "Low"
        }