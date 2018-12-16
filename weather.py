#-*-coding:utf-8-*
import requests

appKey = "37720873-7699-419c-8520-b224518698b4"
#appKey = "c0fdb29b-a503-4503-98a8-e17070dbfe70"

url_minutely = "https://api2.sktelecom.com/weather/current/minutely"
url_forecast= "https://api2.sktelecom.com/weather/forecast/3days"

headers = {
	'Content-Type': 'application/json; charset = utf-8',
	'appKey': appKey
}
params = {
        "version": "1", "city": "서울", "county": "용산구", "village": "청파동3가"
}

error = "error"


def requestForecastTomprec():

	response = requests.get(url_forecast, params=params, headers=headers)

	if response.status_code == 200:

		response_body = response.json()

		forecast_data = response_body['weather']['forecast3days'][0]

		timeRelease = forecast_data['timeRelease']

                grid_city = forecast_data['grid']['city']
                grid_county = forecast_data['grid']['county']
        	grid_village = forecast_data['grid']['village']

        	for_type = forecast_data['fcst3hour']['precipitation']['type7hour']

                if for_type == '0':
                        type_str = "no rain"
                elif for_type == '1':
                        type_str = "rain"
                elif for_type == '2':
                        type_str = "rain or snow"
                elif for_type == '3':
                        type_str = "snow"

                return type_str
		
	else:
		return error



def requestForecastTomtemp():

	response = requests.get(url_forecast, params=params, headers=headers)

	if response.status_code == 200:

		response_body = response.json()

		forecast_data = response_body['weather']['forecast3days'][0]

		timeRelease = forecast_data['timeRelease']

                tmax2day = forecast_data['fcstdaily']['temperature']['tmax2day'][0:3]
                tmin2day = forecast_data['fcstdaily']['temperature']['tmin2day'][0:3]
	
        	fortemp_str = "min " + tmax2day + " max "+ tmin2day

                return fortemp_str
		
        else:
                return error

def requestCurrentTemp():
        
	response = requests.get(url_minutely, params = params, headers = headers)
                                
	if response.status_code == 200:
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]

		timeObservation = weather_data['timeObservation']

                temperature_tmax = weather_data['temperature']['tmax']
        	temperature_tmin = weather_data['temperature']['tmin']

                #time_str = timeRelease
                temp_str = 'min ' + temperature_tmin + ' max ' + temperature_tmax


                return temp_str

	else:
		return error


def requestCurrentPrec():

	response = requests.get(url_minutely, params = params, headers = headers)
                                
	if response.status_code == 200:
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]

		timeObservation = weather_data['timeObservation']
                precipitation_type = weather_data['precipitation']['type']
                precipitation_sinceOntime = weather_data['precipitation']['sinceOntime']

                if precipitation_type == '0':
                        prec = "no rain"
                elif precipitation_type == '1':
                        prec = "rain"
        	elif precipitation_type == '2':
                	prec = "rain or snow"
                elif precipitation_type == '3':
                        prec = "snow"

                return prec

	else:
		return error

if __name__ == "__main__":
        print(requestCurrentTemp())
        print(requestCurrentPrec())
        print(requestForecastTomtemp())
        print(requestForecastTomprec())
