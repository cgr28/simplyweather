# file containing function and variables
import os
import datetime

if os.path.exists('./config/secret.py'):
    from config.secret import *
else:
    API_KEY = os.environ['API_KEY']

# returns time in h:m p format
def format_time(time):
    return datetime.datetime.fromtimestamp(time).strftime("%I:%M %p")

def format_day(day):
    return datetime.datetime.fromtimestamp(day).strftime("%A")    

# returns weather data from given location using openweathermap API
def get_page(request, type="weather", cookie=None):
    # no state and country=US by default
    ctry = ",US"
    state = ""

    if cookie:
        id = request.COOKIES[cookie]
        page = f"https://api.openweathermap.org/data/2.5/weather?id={id}&appid={API_KEY}&units=imperial"
        return page
    if "lat" in request.GET and "long" in request.GET:
        lat = request.GET["lat"]
        long = request.GET["long"]
        page = f"https://api.openweathermap.org/data/2.5/{type}?lat={lat}&lon={long}&appid={API_KEY}&units=imperial"
    elif "city" in request.GET:
        city = request.GET["city"]
        if "state" in request.GET:
            state = "," + request.GET["state"]
        if "ctry" in request.GET:
            ctry = "," + request.GET["ctry"]
        page = f"https://api.openweathermap.org/data/2.5/{type}?q={city}{state}{ctry}&appid={API_KEY}&units=imperial"
    elif "id" in request.GET:
        id = request.GET["id"]
        page = f"https://api.openweathermap.org/data/2.5/{type}?id={id}&appid={API_KEY}&units=imperial"
    else:
        #print("here")
        return None
    return page

# takes wind direction in degrees as param and returns cardinal directions
def get_card_dir(deg):
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

# checks to ensure the api call didnt result in any errors
def error_check(cod):
    context = {"message": "No errors."}
    err = False

    if cod == "404":
            context = {"message": "The city you entered DNE."}
            err = True
    elif cod == "429":
            context = {"message": "Try searching again in a few seconds."}
            err = True
    
    return err, context
    

# dictionary of containing each icon id and its corresponding image name
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