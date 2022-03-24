class Location:

    def __init__(self, data):
        self.data = data

    def get_cod(self):
        return self.data["cod"]
    
    def get_city(self):
        return self.data["name"]
    
    def get_country(self):
        return self.data["sys"]["country"]

    def get_id(self):
        return self.data["id"]

# object for the current weather 
class Current(Location):

    def get_weather(self):
        return self.data["weather"][0]["description"]

    def get_temp(self):
        return self.data["main"]["temp"]

    def get_feels_like(self):
        return self.data["main"]["feels_like"]

    def get_humidity(self):
        return self.data["main"]["humidity"]
    
    def get_wind_speed(self):
        return self.data["wind"]["speed"]

    def get_wind_dir(self):
        return self.data["wind"]["deg"]
    
    def get_sunrise(self):
        return self.data["sys"]["sunrise"]
    
    def get_sunset(self):
        return self.data["sys"]["sunset"]
    
    def get_icon(self):
        return self.data["weather"][0]["icon"]
    
    def get_visibility(self):
        return self.data["visibility"]
    
    def get_pressure(self):
        return self.data["main"]["pressure"]
    
    def get_clouds(self):
        return self.data["clouds"]["all"]
    
# object for the trihoral weather
class Trihoral(Location):
    
    #overriding methods from location
    def __init__(self, data):
        super().__init__(data)
        self.list = self.data["list"] #contains weather data for each hour
        self.hour = self.Hour(0, self)

    def get_city(self):
        return self.data["city"]["name"]
    
    def get_id(self):
        return self.data["city"]["id"]
    
    def get_country(self):
        return self.data["city"]["country"]
    
    # gets weather data for the ith hour
    class Hour:

        def __init__(self, hour, trihoral):
            self.hour = hour
            self.list = trihoral.list
            self.hour_data = self.list[hour]

        def datetime(self):
            return self.hour_data["dt"]
        
        def weather(self):
            return self.hour_data["weather"][0]["main"]

        def temp(self):
            return self.hour_data["main"]["temp"]
        
        def icon(self):
            return self.hour_data["weather"][0]["icon"]
        
        def change_hour(self, hour):
            self.hour = hour
            self.hour_data = self.list[hour]

