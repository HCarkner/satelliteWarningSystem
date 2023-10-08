import math
import requests
from threading import Timer

# Function to calculate the Haversine distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

fireLat = -17.57473
fireLong = 126.3464
villageLat = -17.829965
villageLong = 127.312927

totalDistance = haversine(fireLat, fireLong, villageLat, villageLong)

url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/debca954cf7428c4d8d5d9d41abe4960/VIIRS_SNPP_NRT/world/1/2023-10-08'
def make_api_request():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
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
