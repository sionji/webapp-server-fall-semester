from datetime import datetime
from bs4 import BeautifulSoup as bs
from mySQL import *
import requests

todaytemp = 0
fine_dust = 0
rain_percent = 0
aux = 1

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

def change_aux (case) :
    global aux
    aux = case
   
    f = open ("./info/auxinfo.txt", "w")
    data = "aux=%d"%case
    f.write (data)
    f.close ()

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

    f = open ("./info/weatherinfo.txt", "w")
    data = "todaytemp=%d\nfine_dust=%d\nrain_percent=%d"%(todaytemp, fine_dust, rain_percent)
    f.write (data)
    f.close ()

def read_aux_info () :
    global aux
    with open ("./info/auxinfo.txt", "r") as file :
        line = None
        line = file.readline ()
        line = line.strip ('\n')
        aux = int (line[4:])

def read_weather_info () :
    global todaytemp, fine_dust, rain_percent
    with open ("./info/weatherinfo.txt", "r") as file :
        line = None
        line = file.readline ()
        line = line.strip ('\n')
        todaytemp = int (line[10:])
        line = file.readline ()
        line = line.strip ('\n')
        fine_dust = int (line[10:])
        line = file.readline ()
        line = line.strip ('\n')
        rain_percent = int (line[13:])

# Check the table is outerward.
def bs_findvalue_rtc_id (tablename) :
    global todaytemp, fine_dust, rain_percent, aux
    is_internal = False
    is_safedust = False
    is_rain = False
    is_warm = False
    # If aux is True, then find value. If not, it will don't.
    result = 0 

    read_weather_info ()
    read_aux_info ()

    # Binary Search Options
    if (tablename != 'dduk') :
        is_internal = True

    if (fine_dust < 81) :
        is_safedust = True

    if (rain_percent > 60) :
        is_rain = True

    if (todaytemp > 10 and todaytemp < 30) :
        is_warm = True

    # Dont traverse DB and dont open.
    if (aux == 0) :
        return 0
    # Dont traverse DB and open door.
    elif (aux == 2) :
        return 1 

    # if aux == 1, then traverse the DB
    elif (is_internal == True) :
        result = mySQL(sqltype='findvalue_rtc_id', tablename=tablename, where=None, value=None, time=None)

    elif (is_internal == False and is_safedust == True and is_rain == False and is_warm == True) :
        result = mySQL(sqltype='findvalue_rtc_id', tablename=tablename, where=None, value=None, time=None)

    else :
        result = 0

    # return value is 1, then open. return value is 0, then do not open.
    return result

def get_weather_now () :
    global todaytemp, fine_dust, rain_percent
    read_weather_info ()
    return todaytemp, fine_dust, rain_percent
    
def get_aux_now () :
    global aux
    read_aux_info ()
    return aux
