#-*-coding:utf-8-*
import requests

appKey = "c0fdb29b-a503-4503-98a8-e17070dbfe70"

url_minutely = "https://api2.sktelecom.com/weather/current/minutely"
url_forecast= "https://api2.sktelecom.com/weather/forecast/3days"

headers = {
	'Content-Type': 'application/json; charset = utf-8',
	'appKey': appKey
}
params = {
        "version": "1", "city": "서울", "county": "용산구", "village": "청파동3가"
}

def forecastprec(weather):

	timeRelease = weather['timeRelease']

	grid_city = weather['grid']['city']
	grig_county = weather['grid']['county']
	grid_village = weather['grid']['village']

	for_type = weather['fcst3hour']['precipitation']['type7hour']

	if for_type == '0':
		type_str = "no rain"
	elif for_type == '1':
		type_str = "rain"
	elif for_type == '2':
		type_str = "rain or snow"
	elif for_type == '3':
		type_str = "snow"

	return type_str

def forecasttemp(weather):
	timeRelease = weather['timeRelease']

	grid_city = weather['grid']['city']
	grig_county = weather['grid']['county']
	grid_village = weather['grid']['village']
	temp_max = weather['fcstdaily']['temperature']['tmax2day']
	temp_min = weather['fcstdaily']['temperature']['tmin2day']
	
	fortemp_str = "min " + temp_min + " max "+ temp_max

	return fortemp_str


def requestForecastTomprec():

	response = requests.get(url_forecast, params=params, headers=headers)

	if response.status_code == 200:

		response_body = response.json()

		forecast_data = response_body['weather']['forecast3days'][0]

		forecastprec(forecast_data)
		
	else:
		error = "Error"
		return error



def requestForecastTomtemp():

	response = requests.get(url_forecast, params=params, headers=headers)

	if response.status_code == 200:

		response_body = response.json()

		forecast_data = response_body['weather']['forecast3days'][0]

		forecasttemp(forecast_data)
		
	else:
		error = "Error"
		return 


def minutelyprec(weather):
	timeObservation = weather['timeObservation']
	station_name = weather['station']['name']
	station_id = weather['station']['id']
	
	station_type = weather['station']['type']
	station_latitude = weather['station']['latitude']
	station_longitude = weather['station']['longitude']
	
	precipitation_type = weather['precipitation']['type']
	precipitation_sinceOntime = weather['precipitation']['sinceOntime']

	if precipitation_type == '0':
		prec = "no rain"
	elif precipitation_type == '1':
		prec = "rain"
	elif precipitation_type == '2':
		prec = "rain or snow"
	elif precipitation_type == '3':
		prec = "snow"

	return prec


def minutelytemp(weather):

	timeObservation = weather['timeObservation']

	temperature_tc = weather['temperature']['tc']
	temperature_tmax = weather['temperature']['tmax']
	temperature_tmin = weather['temperature']['tmin']

	station_name = weather['station']['name']
	station_id = weather['station']['id']

	station_type = weather['station']['type']
	station_latitude = weather['station']['latitude']
	station_longitude = weather['station']['longitude']

	#time_str = timeRelease
	temp_str = 'min ' + temperature_tmin + ' max ' + temperature_tmax

	return temp_str


def requestCurrentTemp():

	response = requests.get(url_minutely, params = params, headers = headers)
                                
	if response.status_code == 200:
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]
		
		minutelytemp(weather_data)

	else:
		error = "Error"
		return error


def requestCurrentPrec():

	response = requests.get(url_minutely, params = params, headers = headers)
                                
	if response.status_code == 200:
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]

		minutelyprec(weather_data)
	else:
		error = "Error"
		return error
