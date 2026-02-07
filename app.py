"""
@file: app.py
@author: Jambaldorj Munkhsoyol
This module defines a Flask web application that provides an API endpoint to fetch weather data and generate summaries
using the Weather API and Gemini API. It handles input validation, error handling, and returns JSON responses to clients.
"""

from flask import Flask, request, jsonify
from weather_api import get_current, get_forecast
from gemini_api import get_gemini_response

app = Flask(__name__)

"""
API endpoint to fetch weather data and generate a summary.
It accepts query parameters for city name, unit of temperature, and number of days to forecast.
It validates the input, fetches current weather and forecast data, generates a summary using the Gemini
API, and returns a JSON response containing the weather data and summary. If any errors occur, it
returns an appropriate error message and status code.
"""
@app.route("/weather")
def weather():
    city = request.args.get("city", "").strip()
    unit = request.args.get("unit", "").strip()
    try:
        days = int(request.args.get("days", "").strip())
    except ValueError:
        return jsonify({"error": "Days must be an integer between 1 and 10"}), 400
    
    try:
        current = get_current(city, unit)
        forecast = get_forecast(city, days, unit)
        
        weather_data = {
            "current": current,
            "forecast": forecast
        }
        
        summary = get_gemini_response(weather_data)
        
        return jsonify({
            "weather_data": weather_data,
            "summary": summary
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)