from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from layout.logic import icons, error_check, get_page, format_time
from layout.Location import Current
import requests
import os

# retrieves api key
if os.path.exists('./config/secret.py'):
   # read secrets from json file
        from config.secret import *
else:
    API_KEY = os.environ['API_KEY']

def index(request):
    data = []
    exists = False
    for cookie in request.COOKIES:
        if cookie[0:2] == "id":
            
            page = get_page(request, "weather", cookie)

            if not page:
                continue

            info = requests.get(page).json()

            weather = Current(info)

            cod = weather.get_cod()

            err, _ = error_check(cod)

            if err:
                continue

            #print(info)
            sunset = format_time(weather.get_sunset())
            sunrise = format_time(weather.get_sunrise())
            icon = icons[weather.get_icon()]

            temp = {
                "weather": weather.get_weather(),
                "temp": weather.get_temp(),
                "city": weather.get_city(),
                "country": weather.get_country(),
                "city_id": weather.get_id(),
                "icon": icon,
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