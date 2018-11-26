#-*-coding:utf-8-*-
import GPIO
import urllib.parse as urlparse
import requests
import json
import time
import threading
    
#미세먼지 데이터 요청
def get_finedust_data():
    
    serviceKey = "&serviceKey=YlLv7z9QhbddC9gnDN3tpQfF5cWKoHUp1eYsAPOldfsF7I60a7JXnNLpEwR%2Byi0QDjAldaccns1aHV4J9tKeKg%3D%3D"
    url_dust = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"
    datainfo = {"sidoName":"서울","pageNo":"2","numOfRows":"1","ver":"1.0","_returnType":"json"}

    #미세먼지 정보 URL
    request_query = url_dust + urlparse.urlencode(datainfo) + serviceKey

    response = requests.get(request_query)

    #요청 성공
    if response.status_code == 200:

        dustData = response.json()                          #json 형태로 데이터를 받음
        
        pm10value = dustData['list'][0]['pm10Value']        #미세먼지 수치
        pm25value = dustData['list'][0]["pm25Value"]        #초미세먼지 수치
        pm10grade = dustData['list'][0]['pm10Grade']        #미세먼지 등급

        return pm10value, pm25value, pm10grade
    
    #오류 발생
    else:
        return 0, 0, 0

        
#미세먼지 정보 LCD출력
def display_value(pm10value, pm25value):
       
    if (pm10value == 0):                                     #오류문구 출력                       
        GPIO.setLCD1("*****ERROR******"," Cannot loading")
        
    else:                                                    #정상수치 출력
        value10 = "Fine dust: " + pm10value
        value25 = "ultra-F.dust:" + pm25value
        GPIO.setLCD1(value10, value25)

#미세먼지 등급
#미세먼지 경고 LCD출력
def display_grade(pm10grade):
     
    if (pm10grade == '0'):                                     #오류문구 출력                       
        GPIO.setLCD1("*****ERROR******"," Cannot loading")
        
    elif (pm10grade == '1'):                                   #좋음
        grade10 = "Grade: GOOD"
        order = "IT'S A CLEAR DAY"
        GPIO.setLCD2(grade10, order)

    elif (pm10grade == '2'):                                   #보통
        grade10 = "Grade: NORMAL"
        order = "IT'S YOUR CHOICE"
        GPIO.setLCD2(grade10, order)
        
    elif (pm10grade == '3'):                                   #나쁨
        grade10 = "Grade: BAD"
        order = "CLOSE THE WINDOW"
        GPIO.setLCD2(grade10, order)
    else:                                                    #매우나쁨
        grade10 = "Grade: VERY BAD"
        order = "DO NOT OPEN!!"
        GPIO.setLCD2(grade10, order)

    
try:

    GPIO.setGPIO()                  #원래 main에서 호출(확임을 위해 임시로 호출)
    GPIO.setUltrasonic()
    
    pm10value, pm25value, pm10grade = get_finedust_data()        #미세먼지 데이터 요청

    
    while True:
        display_value(pm10value, pm25value)
        dist = GPIO.distance()
        
        if (dist > 20):
            th1 = threading.Thread(target=display_grade(pm10grade))
            th2 = threading.Thread(target=GPIO.setPiezo)

            th1.start()
            th2.start()
            
except KeyboardInterrupt:
    pass

finally:
    GPIO.lcd_init()
    GPIO.GPIO.cleanup()
    
