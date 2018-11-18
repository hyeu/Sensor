# -*- coding: utf-8 -*- 
import urllib.request as rqst
import urllib.parse as par
import json



def get_finedust_data():
    #rqst = urllib.request
    #par = urllib.parse
    parameter = {par.quote_plus("sidoName"):"서울", par.quote_plus("pageNo"):"6", par.quote_plus("numOfRows"):"1",par.quote_plus("ServiceKey"): "YlLv7z9QhbddC9gnDN3tpQfF5cWKoHUp1eYsAPOldfsF7I60a7JXnNLpEwR%2Byi0QDjAldaccns1aHV4J9tKeKg%3D%3D", par.quote_plus("ver"):"1.0"}
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"

    request = rqst.urlopen(url + par.urlencode(parameter))
    request.get_method = lambda: "GET"
    response_body = request.read()
    print(url + par.urlencode(parameter))
    print(response_body)

try:
    get_finedust_data()

finally:
    pass
