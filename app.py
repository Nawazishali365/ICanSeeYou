from flask import Flask, render_template_string
import requests
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch location data
    locURL = 'https://ipinfo.io/json'
    location = urlopen(locURL)
    YourLoc = json.load(location)
    cityName = YourLoc.get('city')

    # Fetch weather data
    apiKey = '98943b1b4b2021db6e7a9f14cb07059b'
    baseURL = 'https://api.openweathermap.org/data/2.5/weather?q='
    completeURL = baseURL + cityName + '&appid=' + apiKey
    response = requests.get(completeURL)
    data = response.json()

    # Extract weather data
    temp = float(data['main']['temp']) - 273.15
    feels_like = float(data['main']['feels_like']) - 273.15
    max_temp = float(data['main']['temp_max']) - 273.15
    min_temp = float(data['main']['temp_min']) - 273.15

    # Extract location data
    location_data = {
        'Your IP': YourLoc.get('ip'),
        'Your City': YourLoc.get('city'),
        'Your Region': YourLoc.get('region'),
        'Your Country': YourLoc.get('country'),
        'Your Location': YourLoc.get('loc'),
        'Your Wifi': YourLoc.get('org'),
        'Your Postal': YourLoc.get('postal'),
        'Your Time Zone': YourLoc.get('timezone')
    }

    # HTML template as a string
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather and Location Information</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
            }
            .container {
                width: 80%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #333;
                color: #fff;
                padding: 10px 0;
                text-align: center;
            }
            table {
                width: 100%;
                margin: 20px 0;
                border-collapse: collapse;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f4f4f4;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            .weather-info, .location-info {
                margin: 20px 0;
            }
            h2 {
                color: #333;
            }
        </style>
        <script>
            window.onload = function() {
                alert("This website will access your location. Do you want to allow it?");
            }
        </script>
    </head>
    <body>
        <header>
            <h1>Weather and Location Information</h1>
        </header>
        <div class="container">
            <div class="weather-info">
                <h2>Current Weather</h2>
                <table>
                    <tr>
                        <th>Attribute</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Current Temperature</td>
                        <td>{{ temp | round(2) }}°C</td>
                    </tr>
                    <tr>
                        <td>Feels Like</td>
                        <td>{{ feels_like | round(2) }}°C</td>
                    </tr>
                    <tr>
                        <td>Maximum Temperature</td>
                        <td>{{ max_temp | round(2) }}°C</td>
                    </tr>
                    <tr>
                        <td>Minimum Temperature</td>
                        <td>{{ min_temp | round(2) }}°C</td>
                    </tr>
                </table>
            </div>    
            <div class="location-info">
                <h2>Your Location Information</h2>
                <table>
                    <tr>
                        <th>Key</th>
                        <th>Value</th>
                    </tr>
                    {% for key, value in location_data.items() %}
                    <tr>
                        <td>{{ key }}</td>
                        <td>{{ value }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    # Render the HTML template with data
    return render_template_string(html_template, temp=temp, feels_like=feels_like, max_temp=max_temp, min_temp=min_temp, location_data=location_data)

if __name__ == '__main__':
    app.run(debug=True)
