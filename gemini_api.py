"""
@file: gemini_api.py
@author: Jambaldorj Munkhsoyol

This module provides functions to interact with the Gemini API to generate
user-friendly summaries of raw weather data. It retrieves the API key from
environment variables, defines a function to generate a summary using the
Gemini API, and handles errors gracefully by raising exceptions with informative messages.
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
Generates a user-friendly summary of raw weather data using the Gemini API.
@param weather_data: A dictionary containing raw weather data.
@return: A string containing the generated summary.
@raises RuntimeError: If there is an error generating the summary.
"""
def get_gemini_response(weather_data):
    prompt = f"""
    Raw weather data is provided below:
    {weather_data}
    Using it, write a short, user-friendly summary of it.
    """

    try:
        response = CLIENT.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating AI summary: {e}")