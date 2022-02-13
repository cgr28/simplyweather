from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404
import requests
import datetime
import os

if os.path.exists('./config/secret.py'):
    from config.secret import *
else:
    API_KEY = os.environ['API_KEY']

# Create your views here.
icons = {
    "01d": "clear-day.svg",
    "01n": "clear-night.svg",
    "02d": "few-cloud-day.svg",
    "02n": "few-cloud-night.svg",
    "03d": "scattered-clouds.svg",
    "03n": "scattered-clouds.svg",
    "04d": "broken-clouds.svg",
    "04n": "broken-clouds.svg",
    "09d": "shower-rain.svg",
    "09n": "shower-rain.svg",
    "10d": "rain-day.svg",
    "10n": "rain-night.svg",
    "11d": "thunderstorm.svg",
    "11n": "thunderstorm.svg",
    "13d": "snow.svg",
    "13n": "snow.svg",
    "50d": "mist.svg",
    "50n": "mist.svg",
}

def get_wind_dir(deg):
    if 330 <= deg <= 360 or 0 <= deg <= 30:
        return "N"
    if 290 <= deg <= 330:
        return "NW"
    if 250 <= deg <= 290:
        return "W"
    if 210 <= deg <= 250:
        return "SW"
    if 150 <= deg <= 210:
        return "S"
    if 110 <= deg <= 150:
        return "SE"
    if 70 <= deg <= 110:
        return "E"
    return "NE"

def current(request):

    ctry = ",US"
    state = ""

    if "lat" in request.GET and "long" in request.GET:
        lat = request.GET["lat"]
        long = request.GET["long"]
        page = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}&units=imperial"
    elif "city" in request.GET:
        city = request.GET["city"]
        if "state" in request.GET:
            state = "," + request.GET["state"]
        if "ctry" in request.GET:
            ctry = "," + request.GET["ctry"]
        page = f"https://api.openweathermap.org/data/2.5/weather?q={city}{state}{ctry}&appid={API_KEY}&units=imperial"
    elif "id" in request.GET:
        id = request.GET["id"]
        page = f"https://api.openweathermap.org/data/2.5/weather?id={id}&appid={API_KEY}&units=imperial"
    else:
        #print("here")
        raise Http404

    info = requests.get(page).json()
    #print(info)

    if info["cod"] == "404":
        context = {"message": info["message"]}
        return render(request, "weather/index.html", context)
    if info["cod"] == "429":
        context = {"message": "Try searching again in a few seconds."}
        return render(request, "weather/index.html", context)

    sunset = datetime.datetime.fromtimestamp(info["sys"]["sunset"]).strftime("%I:%M %p")
    sunrise = datetime.datetime.fromtimestamp(info["sys"]["sunrise"]).strftime("%I:%M %p")
    data = {
        "weather": info["weather"][0]["description"],
        "temp": info["main"]["temp"],
        "feels_like": info["main"]["feels_like"],
        "humidity": info["main"]["humidity"],
        "wind_speed": info["wind"]["speed"],
        "wind_dir": get_wind_dir(int(info["wind"]["deg"])),
        "city": info["name"],
        "country": info["sys"]["country"],
        "id": info["id"],
        "sunrise": sunrise,
        "sunset": sunset,
        "icon": icons[info["weather"][0]["icon"]],
        "visibility": info["visibility"],
        "pressure": info["main"]["pressure"],
        "cloud": info["clouds"]["all"],
    }

    context = {"data": data}

    return render(request, "weather/current.html", context)

def tri_hourly(request):

    ctry = ""
    state = ""

    if "lat" in request.GET and "long" in request.GET:
        lat = request.GET["lat"]
        long = request.GET["long"]
        page = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={API_KEY}&units=imperial"
    elif "city" in request.GET:
        city = request.GET["city"]
        if "state" in request.GET:
            state = "," + request.GET["state"]
        if "ctry" in request.GET:
            ctry = "," + request.GET["ctry"]
        page = f"https://api.openweathermap.org/data/2.5/forecast?q={city}{state}{ctry}&appid={API_KEY}&units=imperial"
    elif "id" in request.GET:
        id = request.GET["id"]
        page = f"https://api.openweathermap.org/data/2.5/forecast?id={id}&appid={API_KEY}&units=imperial"
    else:
        raise Http404

    info = requests.get(page).json()
    #print(info)
    if info["cod"] == "404":
        context = {"message": info["message"]}
        return render(request, "weather/index.html", context)
    if info["cod"] == "429":
        context = {"message": "Try searching again in a few seconds."}
        return render(request, "weather/index.html", context)

    context = {
        "id": info["city"]["id"],
        "city": info["city"]["name"],
        "country": info["city"]["country"],
        "data": [],
    }
    i = 0

    while i < 30:
        obj = info["list"][i]
        time = datetime.datetime.fromtimestamp(obj["dt"]).strftime("%I:%M %p")
        day = datetime.datetime.fromtimestamp(obj["dt"]).strftime("%A")
        data = {
            "time": time,
            "day": day,
            "weather": obj["weather"][0]["main"],
            "temp": obj["main"]["temp"],
            "icon": icons[obj["weather"][0]["icon"]],
        }
        context["data"].append(data)
        i += 1

    
    return render(request, "weather/tri-hourly.html", context)

def index(request):
    context = {"message": "Try using the search to find the weather."}
    return render(request, "weather/index.html", context)
    