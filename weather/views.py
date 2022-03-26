from django.shortcuts import render
from django.http import Http404
import requests
from layout.Location import Current, Trihoral
from layout.logic import icons, get_card_dir, get_page, error_check, format_time, format_day

# Create your views here.

# the view for the current forecast
def current(request):
    page = get_page(request, "weather")

    if not page:
        raise Http404

    # data from openweathermap converted to json
    info = requests.get(page).json()
    #print(info)

    weather = Current(info)

    cod = weather.get_cod()

    err, context = error_check(cod)

    if err:
        return render(request, "weather/index.html", context)


    sunset = format_time(weather.get_sunset())
    sunrise = format_time(weather.get_sunrise())
    wind_dir = get_card_dir(int(weather.get_wind_dir()))
    icon = icons[weather.get_icon()]

    data = {
        "weather": weather.get_weather(),
        "temp": weather.get_temp(),
        "feels_like": weather.get_feels_like(),
        "humidity": weather.get_humidity(),
        "wind_speed": weather.get_wind_speed(),
        "wind_dir": wind_dir,
        "city": weather.get_city(),
        "country": weather.get_country(),
        "id": weather.get_id(),
        "sunrise": sunrise,
        "sunset": sunset,
        "icon": icon,
        "visibility": weather.get_visibility(),
        "pressure": weather.get_pressure(),
        "cloud": weather.get_clouds(),
    }

    context = {"data": data}

    return render(request, "weather/current.html", context)

# view for the trihoral(formerly trihourly) forecast
def tri_hourly(request):
    page = get_page(request, "forecast") 

    if not page:
        raise Http404

    info = requests.get(page).json()
    #print(info)

    weather = Trihoral(info)

    cod = weather.get_cod()

    err, context = error_check(cod)

    if err:
        return render(request, "weather/index.html", context)

    context = {
        "id": weather.get_id(),
        "city": weather.get_city(),
        "country": weather.get_country(),
        "data": [],
    }

    for i in range(30):
        hour = weather.hour
        hour.change_hour(i)
        time = format_time(hour.datetime())
        day = format_day(hour.datetime())

        data = {
            "time": time,
            "day": day,
            "weather": hour.weather(),
            "temp": hour.temp(),
            "icon": icons[hour.icon()],
        }

        context["data"].append(data)

    
    return render(request, "weather/tri-hourly.html", context)

def index(request):
    context = {"message": "Try using the search to find the weather."}
    return render(request, "weather/index.html", context)
    