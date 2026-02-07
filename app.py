from flask import Flask, request, jsonify
from weather_api import get_current, get_forecast
from gemini_api import get_gemini_response

app = Flask(__name__)

@app.route("/weather")
def weather():
    city = request.args.get("city")
    unit = request.args.get("unit", "C")
    days = int(request.args.get("days", 3))

    if not city:
        return jsonify({"error": "City is required"}), 400
    
    current = get_current(city, unit)
    forecast = get_forecast(city, days, unit)

    if not current or not forecast:
        return jsonify({"error": "Error fetching weather data"}), 500
    
    weather_data = {
        "current": current,
        "forecast": forecast
    }

    return jsonify({
        "data": weather_data,
        "summary": get_gemini_response(weather_data)
    })

if __name__ == "__main__":
    app.run(debug=True)