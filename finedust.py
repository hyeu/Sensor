# -*- coding: utf-8 -*- 
import urllib.request as rqst
import urllib.parse as par
import json

def get_finedust_data():
    Key = "&serviceKey=YlLv7z9QhbddC9gnDN3tpQfF5cWKoHUp1eYsAPOldfsF7I60a7JXnNLpEwR%2Byi0QDjAldaccns1aHV4J9tKeKg%3D%3D"
    params = {"sidoName":"서울","pageNo":"6","numOfRows":"1","ver":"1.0","_returnType":"json"}
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"

    request = rqst.urlopen(url + par.urlencode(params) + Key)
    response = request.read()

    dustData = json.loads(response)

    finedust = dustData['list'][0]['pm10Value']
    fine_particulate_matter = dustData['list'][0]["pm25Value"]
    station = dustData['list'][0]['stationName']

    location = "<" + station + "의 현재 미세먼지 농도>"
    notice1 = '* 미세먼지 농도:' + finedust
    notice2 = '* 초미세먼지 농도:' + fine_particulate_matter 

    print(location)
    print(notice1, notice2, sep="\n")
   
try:
    get_finedust_data()

finally:
    pass
