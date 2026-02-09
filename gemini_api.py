"""
@file: gemini_api.py
@author: Jambaldorj Munkhsoyol
This module provides functions to interact with the Gemini API to generate
user-friendly summaries of weather data. It retrieves the API key from environment
variables, defines a function to generate summaries based on raw weather data,
and handles errors gracefully by raising exceptions with informative messages.
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
Generates a user-friendly summary of the provided weather data using the Gemini API.
@param weather_data: A dictionary containing raw weather data (current and forecast).
@return: A string containing the generated summary.
@raises ValueError: If the input weather data is empty.
@raises RuntimeError: If there is an error generating the summary.
"""
def get_gemini_response(weather_data):
    if not weather_data:
        raise ValueError("Weather data cannot be empty")

    prompt = f"""
    Raw weather data is provided below:
    {weather_data}

    Using it, write a short, user-friendly insight based on the conditions, including:
    - How someone should dress
    - Whether they should bring an umbrella
    - If conditions are good for outdoor activities
    - Any safety considerations for extreme heat, cold, wind, or rain

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
        raise RuntimeError(f"Error generating AI summary: {e}")