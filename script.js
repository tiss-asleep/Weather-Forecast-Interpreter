/**
 * @file: script.js
 * @author: Jambaldorj Munkhsoyol
 * This script handles the interaction between the user interface and the backend API
 * for fetching and displaying weather data. It listens for user input, makes API requests,
 * and updates the DOM with the results or error messages.
 */

const API_URL = 'http://127.0.0.1:5000/weather';

// DOM elements
const CITY = document.getElementById('city');
const UNIT = document.getElementById('unit');
const DAYS = document.getElementById('days');
const GET_WEATHER_BUTTON = document.getElementById('getWeatherButton');
const OUTPUT = document.getElementById('output');

/**
 * Fetches weather data from the backend API based on user input and updates the UI accordingly.
 * Validates input, handles loading state, and displays results or errors.
 */
async function getWeather() {
    const city = CITY.value.trim();
    const unit = UNIT.value;
    const days = DAYS.value;
    
    if (!city) {
        displayError('Please enter a city name.');
        return;
    }
    
    OUTPUT.innerHTML = '<div class="loading">Loading weather data...</div>';
    GET_WEATHER_BUTTON.disabled = true;
    
    try {
        const url = `${API_URL}?city=${encodeURIComponent(city)}&unit=${unit}&days=${days}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (!response.ok) {
            displayError(data.error || 'An error occurred while fetching weather data.');
            return;
        }
        
        displayWeather(data, city, unit);
    } catch (error) {
        displayError('Not connected to the server.');
    } finally {
        GET_WEATHER_BUTTON.disabled = false;
    }
}

/**
 * Renders the weather data on the page, including current conditions, forecast, and AI summary.
 * @param data The weather data returned from the API, including current conditions, forecast, and AI summary.
 * @param city The name of the city for which the weather data was fetched. 
 * @param unit The unit of measurement for temperature (°C or °F) to display in the results. 
 */
function displayWeather(data, city, unit) {
    const {summary, weather_data} = data;
    const {current, forecast} = weather_data;
    
    let html = `
        <div class="weather-result">
            <h2>Weather for ${city}</h2>
            
            <div class="current-weather">
                <h3>Current Conditions</h3>
                <p><strong>Temperature:</strong> ${current.temperature}${unit}</p>
                <p><strong>Condition:</strong> ${current.condition}</p>
                <p><strong>Humidity:</strong> ${current.humidity}%</p>
                <p><strong>Wind Speed:</strong> ${current.wind_kph} km/h</p>
            </div>
            
            <div class="forecast">
                <h3>${forecast.length}-Day Forecast</h3>
                <div class="forecast-grid">
    `;
    
    forecast.forEach(day => {
        html += `
            <div class="forecast-day">
                <p class="date">${formatDate(day.date)}</p>
                <p class="condition">${day.condition}</p>
                <p class="temps">${day.min_temp} - ${day.max_temp}${unit}</p>
                <p class="rain">${day.chance_of_rain}%</p>
            </div>
        `;
    });
    
    html += `
                </div>
            </div>
            
            <div class="ai-summary">
                <h3>AI Summary</h3>
                <p>${summary}</p>
            </div>
        </div>
    `;
    
    OUTPUT.innerHTML = html;
}

/**
 * Displays an error message in the output area when something goes wrong.
 * @param message The error message to display to the user, providing feedback on what went wrong.
 */
function displayError(message) {
    OUTPUT.innerHTML = `
        <div class="error">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

/**
 * Formats a date string from the API into a more user-friendly format for display in the forecast section.
 * @param dateStr A date string in the format "YYYY-MM-DD" that needs to be formatted for display. 
 * @returns The formatted date string in the format "Mon DD".
 */
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = {
        month: 'short',
        day: 'numeric'
    };
    return date.toLocaleDateString('en-US', options);
}

// Event listener for the "Get Weather" button to trigger the weather fetching process when clicked.
GET_WEATHER_BUTTON.addEventListener('click', getWeather);