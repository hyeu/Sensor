#-*-coding:utf-8-*-

import RPi.GPIO as GPIO
import time
import threading
import requests

def setGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

#----------------------LCD-------------------------
#Define GPIO to LCD mapping
LCD_E = 26
LCD_RS = 23
LCD_RW = 24
LCD_D4 = 17
LCD_D5 = 18
LCD_D6 = 27
LCD_D7 = 22

#Define some device constants
LCD_WIDTH = 16  #Maximum characters per line
LCD_CHR = True
LCD_CMD = False
    
LCD_LINE_1 = 0x80 #LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 #LCD RAM address for the 2nd line

#Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

appKey = "c0fdb29b-a503-4503-98a8-e17070dbfe70"

url_minutely = "https://api2.sktelecom.com/weather/current/minutely"
url_forecast= "https://api2.sktelecom.com/weather/forecast/3days"

headers = {
	'Content-Type': 'application/json; charset = utf-8',
	'appKey': appKey
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

	print(type_str)
	return type_str

def forecasttemp(weather):
	timeRelease = weather['timeRelease']

	grid_city = weather['grid']['city']
	grig_county = weather['grid']['county']
	grid_village = weather['grid']['village']
	temp_max = weather['fcstdaily']['temperature']['tmax2day']
	temp_min = weather['fcstdaily']['temperature']['tmin2day']
	
	fortemp_str = "min " + temp_min + " max "+ temp_max

	print(fortemp_str)
	return fortemp_str


def requestForecastTomprec(city, county, village):

	params ={
	"version": "1", "city": city, "county": county, "village": village, "foretxt": "N" 
	}

	response = requests.get(url_forecast, params=params, headers=headers)

	if response.status_code == 200:

		response_body = response.json()

		forecast_data = response_body['weather']['forecast3days'][0]

		forecastprec(forecast_data)
		
	else:
		error = "Error"
		return error



def requestForecastTomtemp(city, county, village):

	params ={
	"version": "1", "city": city, "county": county, "village": village, "foretxt": "N" 
	}

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

	print(prec)
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

	print(temp_str)
	return temp_str


def requestCurrentTemp(city, county, village):
	
	params = {
	"version": "1", "city": city, "county": county, "village": village
	}

	response = requests.get(url_minutely, params = params, headers = headers)
                                
	if response.status_code == 200:
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]
		
		minutelytemp(weather_data)

	else:
		error = "Error"
		return error


def requestCurrentPrec(city, county, village):

	params = {
	"version": "1", "city": city, "county": county, "village": village
	}

	response = requests.get(url_minutely, params = params, headers = headers)
                                
	if response.status_code == 200:
		response_body = response.json()

		weather_data = response_body['weather']['minutely'][0]

		minutelyprec(weather_data)
	else:
		error = "Error"
		return error

def setLCD1():
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    #GPIO.setup(LCD_RW, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    #initialise display
    lcd_init()

    while True:
        #창문 LCD 첫번째 표시 (미세먼지) / 3초 동안 지속
        lcd_string("today weather", LCD_LINE_1)
        lcd_string(requestCurrentTemp('서울', '용산구', '청파동3가'), LCD_LINE_2)
		lcd_string(requestCurrentPrec('서울', '용산구', '청파동3가'), LCD_LINE_2)
        time.sleep(3)
        
        #창문 LCD 두번째 표시 (오늘날씨) / 3초 동안 지속
        lcd_string("tomorrow weather", LCD_LINE_1)
        lcd_string(requestForecastTomtemp('서울','용산구','청파동3가'), LCD_LINE_2)
		lcd_string(requrestForecastTomprec('서울','용산구','청파동3기'), LCD_LINE_2) 
        time.sleep(3)

        #창문 LCD 세번째 표시 (내일날씨) / 3초 동안 지속
        lcd_string("1234567890123456", LCD_LINE_1)
        lcd_string("1234567890123456", LCD_LINE_2)
        time.sleep(3)

#창문 열렸을 때 LCD 기본값
def setLCD2():
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    #GPIO.setup(LCD_RW, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    #initialise display
    lcd_init()

    #창문 열렸을 때 표시할 문구 입력
    lcd_string("1234567890123456", LCD_LINE_1)
    lcd_string("CLOSE THE WINDOW", LCD_LINE_2)
    time.sleep(5)
        
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)

    #High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
    #toggle 'enable' pin
    lcd_toggle_enable()

    #Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
    #toggle 'enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH," ") #left side
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
#--------------------------------------------------
#-------------setUltrasonic&setPiezo---------------
GPIO_TRIGGER = 0
GPIO_ECHO = 1

def setUltrasonic():
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    while True:    
        dist = distance()
        print "Measured Distance = %.1f cm" %dist
        time.sleep(0.5)
        
    #창문 열렸을 때 거리 기준값 설정
        if (dist >= 20):
            setPiezo()
            setLCD2()

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

    return distance

def setPiezo():
    GPIO_PIEZO = 13
    GPIO.setup(GPIO_PIEZO, GPIO.OUT)

    p = GPIO.PWM(GPIO_PIEZO, 100)
    p.start(100)
    p.ChangeDutyCycle(90)
    
    #창문 열렸을 때 소리 지속 시간 설정
    for i in range(0, 3, 1):
        for j in range(0, 3, 1):        
            p.ChangeFrequency(392)
            time.sleep(0.3)
    p.stop()
#--------------------------------------------------
if __name__=='__main__':
    try:
        setGPIO()
        th = threading.Thread(target=setUltrasonic)
        th.start()
        while True:
            setLCD1()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_init()
        GPIO.cleanup()