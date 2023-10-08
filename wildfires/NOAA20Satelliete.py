import math
import requests
from threading import Timer
def haversine(lat1, lon1, lat2, lon2):  
    R = 6371.0
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_bearing(lat1, lon1, lat2, lon2):

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(bearing/45) % 8
    direction = directions[index]
    return direction

fireLat = -17.57473
fireLong = 126.3464
villageLat = -17.829965
villageLong = 127.312927

totalDistance = haversine(fireLat, fireLong, villageLat, villageLong)
villageDirection = calculate_bearing(villageLat, villageLong, fireLat, fireLong)

url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/1ffb6fb3a0871a613459afa9a959bc9a/VIIRS_NOAA20_NRT/world/1/2023-10-08'
def make_api_request():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
            print(f"Fire detected: {villageDirection} ")
            if totalDistance > 150 and totalDistance <= 200:
                print('Low Risk')
            elif totalDistance > 100 and totalDistance <= 150:
                print("Medium Risk")
            elif totalDistance > 50 and totalDistance <= 100:
                print("High Risk")
            elif totalDistance >= 0 and totalDistance <= 50:
                print('Severe risk')
        else:
            print(f"API request failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
def schedule_api_request():
    make_api_request()
    t = Timer(215, schedule_api_request)
    t.start()
if __name__ == '__main__':
    schedule_api_request()
