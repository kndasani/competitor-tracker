import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "your_gemini_api_key_here":
    print("Error: GEMINI_API_KEY is missing or unchanged in .env file.")
else:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello! Confirm with 'Gemini API is ready.'",
        )
        print(response.text.strip())
    except Exception as e:
        print(f"Error calling Gemini API: {e}")