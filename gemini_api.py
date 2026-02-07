import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash-lite"

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
        model=MODEL_NAME,
        contents=prompt
    ).text