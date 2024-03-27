from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home Page")


@app.route("/weather")
def weather():
    city = request.args.get("city")
    
    if not bool(city.strip()):
        city = "Abu Dhabi"
        
    weather_data = get_current_weather(city)
    if weather_data["cod"] != 200:
        return render_template("city_not_found.html")
        
    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data["main"]["temp"]:.1f}", 
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
    )


if __name__ == "__main__":
    print("Server is running on port 8000")
    serve(app, host="0.0.0.0", port=8000)
    