from datetime import datetime
from bs4 import BeautifulSoup as bs
from mySQL import *
import requests

todaytemp = 0
fine_dust = 0
rain_percent = 0
aux = True

def weather_now () :
    global todaytemp, fine_dust, rain_percent
    html = requests.get('https://search.naver.com/search.naver?query=weather')
    soup = bs (html.text, 'html.parser')
    temp = str(soup.find ('span',{'class':'todaytemp'}).text)
    data1 = soup.find ('div',{'class':'detail_box'})
    data2 = data1.findAll('dd')
    dust = data2[0].find ('span',{'class':'num'}).text
    html = requests.get('https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=06230111')
    soup = bs (html.text, 'html.parser')
    data3 = soup.select ('#content > div.w_now2 > ul > li:nth-child(1) > div > p > strong')
    rain = str(data3[0].text)
    print ("Now Temp : "+temp+", Dust : "+dust+", Rain : "+rain+"%")
    todaytemp = int(temp)
    fine_dust = int(dust[0:2])
    rain_percent = int(rain)

def change_weather_case (case) :
    global todaytemp, fine_dust, rain_percent
    # Case sensitivity
    if (case == 0) :
        weather_now()
    elif (case == 1) :
        todaytemp = 28
        fine_dust = 17
        rain_percent = 0
    elif (case == 2) :
        todaytemp = 15
        fine_dust = 32 
        rain_percent = 80
    elif (case == 3) :
        todaytemp = -17
        fine_dust = 22
        rain_percent = 30
    elif (case == 4) :
        todaytemp = 26
        fine_dust = 99
        rain_percent = 15

def change_aux (case) :
    global aux
    if (case == 0) :
        aux = False
    else :
        aux = True

# Check the table is outerward.
def bs_findvalue_rtc_id (tablename) :
    global todaytemp, fine_dust, rain_percent, aux
    is_internal = False
    is_safedust = False
    is_rain = False
    is_warm = False
    # If aux is True, then find value. If not, it will don't.
    result = 0 

    # Binary Search Options
    if (tablename != 'dduk') :
        is_internal = True

    if (fine_dust < 81) :
        is_safedust = True

    if (rain_percent > 60) :
        is_rain = True

    if (todaytemp > 10 and todaytemp < 30) :
        is_warm = True

    if (aux == False) :
        return result

    elif (is_internal == True) :
        result = mySQL(sqltype='findvalue_rtc_id', tablename=tablename, where=None, value=None, time=None)

    elif (is_internal == False and is_safedust == True and is_rain == False and is_warm == True) :
        result = mySQL(sqltype='findvalue_rtc_id', tablename=tablename, where=None, value=None, time=None)

    else :
        result = 0

    return result

def get_weather_now () :
    global todaytemp, fine_dust, rain_percent
    return todaytemp, fine_dust, rain_percent
    
def get_aux_now () :
    global aux
    return aux
