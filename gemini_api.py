"""
@file: gemini_api.py
@author: Jambaldorj Munkhsoyol
This module provides functionality to interact with the Gemini API to generate
user-friendly insights based on raw weather data. It retrieves the API key from
environment variables, constructs a prompt for the AI model, and returns a concise summary
of weather conditions and recommendations for users.
"""

import os
from google import genai

MODEL_NAME = "gemini-2.5-flash-lite"

"""
Retrieves the Gemini API key from environment variables.
@return: The Gemini API key as a string.
@raises RuntimeError: If the GEMINI_API_KEY environment variable is not set.
"""
def _get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return api_key

CLIENT = genai.Client(api_key=_get_api_key())

"""
Generates a user-friendly insight based on raw weather data using the Gemini API.
@param weather_data: A string containing raw weather data.
@return: User-friendly insights of the weather conditions as a string.
@raises ValueError: If the weather_data parameter is empty.
@raises RuntimeError: If there is an error generating the AI insights.
"""
def get_gemini_response(weather_data):
    if not weather_data:
        raise ValueError("Weather data cannot be empty")

    prompt = f"""
    Raw weather data is provided below:
    {weather_data}

    Using it, write a short, user-friendly insight based on the conditions, including things such as:
    - How someone should dress
    - Whether they should bring an umbrella
    - If conditions are good for outdoor activities
    - Any safety considerations for extreme heat, cold, wind, or rain

    Feel free to include any other relevant insights that a user might find helpful based on the weather data.

    Important:
    - Do not include technical details or raw data
    - Focus on clear, simple explanations for a general audience
    - Use a friendly and conversational tone
    - Do not use markdown, emojis, HTML tags, or special characters
    - Write in plain text only
    - Keep the response concise but helpful
    """

    try:
        response = CLIENT.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating AI insights: {e}")