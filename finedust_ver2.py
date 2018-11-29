#-*-coding:utf-8-*-
import requests
import json

#서비스키
serviceKey = "&serviceKey=YlLv7z9QhbddC9gnDN3tpQfF5cWKoHUp1eYsAPOldfsF7I60a7JXnNLpEwR%2Byi0QDjAldaccns1aHV4J9tKeKg%3D%3D"
#기본 url
url_dust = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?" + serviceKey
#기본 지역 설정
datainfo = {"sidoName":"서울","pageNo":"2","numOfRows":"1","ver":"1.0","_returnType":"json"}


#미세먼지 정보 LCD출력
def display_value10():

    response = requests.get(url_dust, params = datainfo)    #미세먼지 데이터 요청
    
    #요청 성공
    if response.status_code == 200:

        dustData = response.json()                          #json타입으로 받은 데이터를 dict로 바꿈
        
        pm10value = dustData['list'][0]["pm10Value"]        #미세먼지 수치

        if (pm10value == '-'):                              #측정값 없을때
            value10 = "No data"
        else:   
            value10 = "Fine dust:" + pm10value              #정상 요청값

        return value10
    
    #요청 실패
    else:
        message = "*****ERROR******"
        return message

#초미세먼지 정보 LCD출력
def display_value25():

    response = requests.get(url_dust, params = datainfo)    #미세먼지 데이터 요청

    #요청 성공
    if response.status_code == 200:

        dustData = response.json()                          #json타입으로 받은 데이터를 dict로 바꿈
        
        pm25value = dustData['list'][0]["pm25Value"]        #초미세먼지 수치

        if (pm25value == '-'):                              #측정값 없을때
            value25 = "No data"
        else:   
            value25 = "Fine dust:" + pm25value              #정상 요청값

        return value25
    
    #요청 실패
    else:
        message = "-Can't loading-"
        return message

#미세먼지 등급 LCD 출력
def grade_state():

    response = requests.get(url_dust, params = datainfo)    #미세먼지 데이터 요청
    

    dustData = response.json()                              #json타입으로 받은 데이터를 dict로 바꿈
    pm10grade = dustData['list'][0]['pm10Grade']            #미세먼지 등급
  

    if (pm10grade == '1'):                                   #좋음
        grade = "Grade: GOOD"
        return grade

    elif (pm10grade == '2'):                                 #보통
        grade = "Grade: NORMAL"
        return grade
        
    elif (pm10grade == '3'):                                 #나쁨
        grade = "Grade: BAD"
        return grade
    
    else:                                                    #매우나쁨
        grade = "Grade: VERY BAD"
        return grade

#미세먼지 경고 LCD출력
def grade_order():
    
    response = requests.get(url_dust, params = datainfo)    #미세먼지 데이터 요청
    

    dustData = response.json()                              #json타입으로 받은 데이터를 dict로 바꿈
    pm10grade = dustData['list'][0]['pm10Grade']            #미세먼지 등급
  

    if (pm10grade == '1'):                                   #좋음
        order = "IT'S A CLEAR DAY"
        return order

    elif (pm10grade == '2'):                                 #보통
        order = "IT'S YOUR CHOICE"
        return order
    
    elif (pm10grade == '3'):                                 #나쁨
        order = "CLOSE THE WINDOW"
        return order
    
    else:                                                    #매우나쁨
        order = "DON'T OPEN!"
        return order

#미세먼지 등급 값 반환
def grade_value():

    response = requests.get(url_dust, params = datainfo)    #미세먼지 데이터 요청
    

    dustData = response.json()                              #json타입으로 받은 데이터를 dict로 바꿈
    pm10grade = dustData['list'][0]['pm10Grade']            #미세먼지 등급
  

    if (pm10grade == '1'):                                   #좋음
        return pm10grade

    elif (pm10grade == '2'):                                 #보통
        return pm10grade
        
    elif (pm10grade == '3'):                                 #나쁨
        return pm10grade
    
    else:                                                    #매우나쁨
        return pm10grade

    
