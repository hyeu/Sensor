import requests

appKey = "c0fdb29b-a503-4503-98a8-e17070dbfe70"

url_minutely = "https://api2.sktelecom.com/weather/current/minutely"
url_forecast= "https://api2.sktelecom.com/weather/forecast/3days"

headers = {
	'Content-Type': 'application/json; charset = utf-8',
	'appKey': appKey
}

def forecast(weather):

	timeRelease = weather['timeRelease']

	grid_city = weather['grid']['city']
	grid_county = weather['grid']['county']
	grid_village = weather['grid']['village']

	temp_max = weather['fcstdaily']['temperature']['tmax2day']
	temp_min = weather['fcstdaily']['temperature']['tmin2day']
	for_type = weather['fcst3hour']['precipitation']['type7hour']

	if for_type == '0':
		type_str = "no rain"
	elif for_type == '1':
		type_str = "rain"
	elif for_type == '2':
		type_str = "rain or snow"
	elif for_type == '3':
		type_str = "snow"

	fortemp_str = 'tomorrow temp'
	fortemp_minmax =temp_min + " "+ temp_max
	forprec_str = 'prob: ' 

	print(fortemp_str)
	print(fortemp_minmax)
	print("precipitation")
	print(type_str)

def requestForecast7hours(city, county, village):

	params ={
	"version": "1", "city": city, "county": county, "village": village, "foretxt": "N" 
	}

	response = requests.get(url_forecast, params=params, headers=headers)

	if response.status_code == 200:

		response_body = response.json()

		forecast_data = response_body['weather']['forecast3days'][0]

		forecast(forecast_data)
	else:
		pass

def minutely(weather):

	timeObservation = weather['timeObservation']

	temperature_tc = weather['temperature']['tc']
	temperature_tmax = weather['temperature']['tmax']
	temperature_tmin = weather['temperature']['tmin']

	station_name = weather['station']['name']
	station_id = weather['station']['id']

	station_type = weather['station']['type']
	station_latitude = weather['station']['latitude']
	station_longitude = weather['station']['longitude']

	precipitation_type = weather['precipitation']['type']
	precipitation_sinceOntime = weather['precipitation']['sinceOntime']

	sky_name  = weather['sky']['name']
	sky_code  = weather['sky']['code']

	if precipitation_type == '0':
		prec = "no rain"
	elif precipitation_type == '1':
		prec = "rain"
	elif precipitation_type == '2':
		prec = "rain or snow"
	elif precipitation_type == '3':
		prec = "snow"

	#time_str = timeRelease
	temp_str = temperature_tc
	temp_str2 = 'min' + temperature_tmin + ',max ' + temperature_tmax

	print("current temp")
	print(temp_str)
	print(temp_str2)
	print(prec)

def requestCurrentWeather(city, county, village):
	
	params = {
	"version": "1", "city": city, "county": county, "village": village
	}

	response = requests.get(url_minutely, params = params, headers = headers)

	# 응답 상태 코드. 200: successful
	if response.status_code == 200:
		# 응답 데이터 받기 ( json 형태 )
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]
		
		minutely(weather_data)
	else:
		pass


if __name__ == '__main__':

	requestForecast7hours('서울', '송파구', '잠실7동')
	requestCurrentWeather('서울','강남구','삼성동')
