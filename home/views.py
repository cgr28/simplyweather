from django.http.response import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import requests
import datetime
import os

if os.path.exists('./config/secret.py'):
   # read secrets from json file
        from config.secret import *
else:
    API_KEY = os.environ['API_KEY']

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

def index(request):
    data = []
    exists = False
    for cookie in request.COOKIES:
        if cookie[0:2] == "id":

            
            id = request.COOKIES[cookie]
            #print(id)
            page = f"http://api.openweathermap.org/data/2.5/weather?id={id}&appid={API_KEY}&units=imperial"
            info = requests.get(page).json()
            if info["cod"] == "404":
                continue
            if info["cod"] == "429":
                continue
            #print(info)
            sunset = datetime.datetime.fromtimestamp(info["sys"]["sunset"]).strftime("%I:%M %p")
            sunrise = datetime.datetime.fromtimestamp(info["sys"]["sunrise"]).strftime("%I:%M %p")
            temp = {
                "weather": info["weather"][0]["main"],
                "temp": info["main"]["temp"],
                "city": info["name"],
                "country": info["sys"]["country"],
                "city_id": info["id"],
                "icon": icons[info["weather"][0]["icon"]],
                "sunrise": sunrise,
                "sunset": sunset,
            }
            data.append(temp)
            exists = True
    #print(exists, data)
    context = {"data":data, "exists":exists}
    if "error" in request.GET:
        if request.GET["error"]  == "lookup":
            context["error"] = "Must enter a city to lookup the weather. Please try again."
        elif request.GET["error"] == "location":
            context["error"] = "There was a problem when trying to get your location. Please make sure you are allowing location."
        else:
            context["error"] = "There has been an error."
    
    return render(request, 'home/index.html', context)

def about(request):
    template = loader.get_template('home/about.html')
    context = {}
    return HttpResponse(template.render(context, request))