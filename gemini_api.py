import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

CLIENT = genai.Client(api_key=API_KEY)

def get_gemini_response(weather_data):
    prompt = f"""
    Raw weather data is provided below:
    {weather_data}
    Using it, write a short, user-friendly summary of it.
    """

    return CLIENT.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    ).text