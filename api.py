import requests

appKey = "c0fdb29b-a503-4503-98a8-e17070dbfe70"

url_hourly = "https://api2.sktelecom.com/weather/current/hourly"
url_minutely = "https://api2.sktelecom.com/weather/current/minutely"

headers = {'Content-Type' : 'application/json; charset=utf-8', 'appKey': appKey}

def hourly(weather):

	humidity = weather['humidity']

	timeRelease = weather['timeRelease']

	temperature_tmax = weather['temperature']['tmax']
	temperature_tc = weather['temperature']['tc']
	temperature_tmin = weather['temperature']['tmin']

	grid_city = weather['grid']['city']
	grid_county = weather['grid']['county']
	grid_village = weather['grid']['village']

	str = '시간별 온도 ' + temperature_tc + ', 최고' + temperature_tmax + ', 최저 ' + temperature_tmin

	print(str)

def requestCueentWeather(city, county, village, isHourly = True):
	params = {"version":"1", "city": city, "county": county, "village": village}

	if isHourly:
		response = requests.get(url_hourly, params=params, headers=headers)
	else:
		response = response.get(url_minutely, params=params, headers=headers)

	if response.status_code == 200:
		response_body = response.json()

		try:
			if isHourly:
				weather_data = response_body['weather']['hourly'][0]
			else:
				weather_data = response_body['weather']['minutely'][0]

			if isHourly:
				hourly(weather_data)
			else:
				minutely(weather_data)

		except:
			pass
	else:
		pass
if __name__== '__main__':

	requestCueentWeather('서울','송파구','잠실7동')
