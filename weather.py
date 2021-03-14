import requests, json
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
import time

temperature = 0
humidity = 0
pressure = 0
report = ''
ip = ''

def getIP():
   global ip
   try:
      ip = requests.get('https://api.ipify.org').text
   except:
      print('could not connect to ipify, retrying...')
      time.sleep(2000)
      getIP()

#get location from ip
getIP()
print(ip)
response = DbIpCity.get(str(ip), api_key='free')
geolocator = Nominatim(user_agent="Your_Name")
location = geolocator.geocode('response.city'.split(' ')[0])
latitude = str(location.latitude)
longitude = str(location.longitude)

print('approximate latitude is ' + latitude)
print('approximate longitude is ' + longitude)


BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = '00f6e237960715dec93a4b29fec1ec9c'
UNIT = 'imperial'#metric, standard
URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + latitude + '&lon=' + longitude + '&units=' + UNIT + '&exclude=hourly,daily&appid=' + API_KEY+''

def getWeather():
   global temperature
   global humidity
   global pressure
   global report

   response = requests.get(URL)
   # checking the status code of the request
   if response.status_code == 200:
      # getting data in the json format
      data = response.json()
      # getting the main dict block
      main = data['current']
      # getting temperature
      temperature = main['temp']
      # getting the humidity
      humidity = main['humidity']
      # getting the pressure
      pressure = main['pressure']
      # weather report
      report = main['weather'][0]['description']

   else:
      # showing the error message
      print("Error in the HTTP request")