#-*- coding : utf-8 -*-
#import official module
from flask import Flask, render_template, url_for, request, redirect
from subprocess import call, PIPE, Popen
from firebase import firebase
from pyfcm import FCMNotification
from datetime import datetime
import requests
import psutil
import json

#import custom module
import binarysearch
from mySQL import *

app = Flask(__name__)

# fire status global variable
fire_pistatus = 0
# maze pointer must be string
maze_i = '20'
maze_j = '40'
#firebase realtime database
thread = None
duckbase = firebase.FirebaseApplication('https://gradeprojectoreo.firebaseio.com/', None)
sionbase = firebase.FirebaseApplication('https://graduate-project-c0c01.firebaseio.com/', None)

def change_fire_case (case) :
    global maze_i, maze_j
    # Case sensitivity
    if (case == 0) :
        maze_i = '20'
        maze_j = '40'

    elif (case == 1) :
        maze_i = '20'
        maze_j = '40'
   
    elif (case == 2) :
        maze_i = '20'
        maze_j = '40'
    
    elif (case == 3) :
        maze_i = '20'
        maze_j = '40'
   
    elif (case == 4) :
        maze_i = '20'
        maze_j = '40'


def fcm_datapush(title, body) : 
    data_message = {
            "message_title" : title,
            "message_body" : body,
            "message_channel" : "EMERGENCY"
            }
    listToken = []
    usertokens = duckbase.get("/users", None)
    for k, v in usertokens.items():
        listToken.append(v["token"])
    push_service = FCMNotification(api_key="AAAAKZIq-gg:APA91bFAQi1T8kZRPMiTFol8NG7undfjGOMjw5ebh5QaF3cLbAZQ_XfxSMEo1nF-uThG7sARbtWoZChtoRjWlxhKFLsGcCYY2TT2h8dkX3VnZGFKP9KlfwOBH1ritnBGabzDftMt2Pv9")
    result = push_service.multiple_devices_data_message(registration_ids=listToken, data_message=data_message)
    return result

#raspi cpu temperature
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1 : output.rindex("'")])


@app.route('/')
def basic():
    return 'Fly to the Moon Graduate Project'

@app.route('/servertime/', methods=['GET'])
def servertime():
    sqltype = 'findtime_id' 
    tablename = request.args.get("table1")
    row = mySQL(sqltype=sqltype, tablename=tablename, where=None, value=None, time=None)
    modtime = str(row[1])
    time_s = modtime[0:2] + '-' + modtime[2:4] + '-' + modtime[4:6]
    #print (time_s)
    todaytemp, fine_dust, rain_percent = binarysearch.get_weather_now ()
    aux = binarysearch.get_aux_now ()
    return render_template('servertime.html', modtime=time_s, tablename=tablename, todaytemp=todaytemp, fine_dust=fine_dust, rain_percent=rain_percent, aux=aux)

@app.route('/fire/<int:input_pistatus>')
def fire_occurs(input_pistatus):
    global fire_pistatus
    # fire_pistatus and input_pistatus is int type data
    if (fire_pistatus == 0 and input_pistatus == 1) :
        fire_pistatus = input_pistatus
        duckbase.patch('/maze/f1', {'i' : "20"})
        duckbase.patch('/maze/f1', {'j' : "40"})
        message = fcm_datapush('Fire Occured!', 'Touch to see evacuation route.')
        print(message)
        return 'Global variable is %d' % fire_pistatus
    
    else :
        return 'Global variable is %d' % fire_pistatus

@app.route('/fire/reset', methods=['GET'])
def fire_reset():
    global fire_pistatus
    fire_pistatus = 0
    return 'Global variable reset to %d' %fire_pistatus

@app.route('/changeweather/<int:case>/')
def ChangeWeather(case):
    binarysearch.change_weather_case (case)
    return 'Weather is now at Case ' + str(case)

@app.route('/changeaux/<int:case>/')
def ChangeAux(case):
    binarysearch.change_aux (case)
    return 'Aux is now at Boolean ' + str(case)

@app.route('/arduino', methods=['GET'])
def arduino():
    global fire_pistatus
    sqltype1 = None
    sqltype2 = None
    table1 = None
    table2 = None
    where1 = None
    where2 = None
    value1 = None
    value2 = None
    time = None
    if (fire_pistatus == 1) :
        # if fire_pistatus is int 1, then return string 1
        return 'y'

    elif request.method == 'GET' :
        sqltype1 = request.args.get("sqltype1")
        sqltype2 = request.args.get("sqltype2")
        table1 = request.args.get("table1")
        table2 = request.args.get("table2")
        where1 = request.args.get("where1")
        where2 = request.args.get("where2")
        value1 = request.args.get("value1")
        value2 = request.args.get("value2")
        time = request.args.get("time")
	
        if ( sqltype1 != None and sqltype1 == 'findvalue_rtc_id' ) :
            result = binarysearch.bs_findvalue_rtc_id (tablename=table1)
        elif ( sqltype1 != None ) :
            result = mySQL(sqltype=sqltype1, tablename=table1, where=where1, value=value1, time=time)

        if ( sqltype2 != None and sqltype2 == 'findvalue_rtc_id' ) : 
            result = binarysearch.bs_findvalue_rtc_id (tablename=table2)
        elif ( sqltype2 != None ) : 
            result = mySQL(sqltype=sqltype2, tablename=table2, where=where2, value=value2, time=time)

        if ( result == 1 ):
            return 'y'
        else :
            return 'n'

    else :
        return "Check your request..."

@app.route('/arduino/web', methods=['GET'])
def arduino_web():
    global fire_pistatus
    sqltype = None
    tablename = None
    where = None
    value = None
    time = None

    if (fire_pistatus == 1) :
        # if fire_pistatus is int 1, then return string 1
        return '1'

    elif request.method == 'GET' :
        sqltype = request.args.get("sqltype1")
        tablename = request.args.get("table1")
        where = request.args.get("where1")
        value = request.args.get("value1")
        time = request.args.get("time")
		
        result = mySQL(sqltype=sqltype, tablename=tablename, where=where, value=value, time=time)

        if (sqltype == 'showall') :
            return render_template('selectdb.html', result=result) 
        elif (sqltype == 'insert'):
            selectedrows = mySQL(sqltype="showall", tablename=tablename, where=where, value=value, time=time)
            return render_template('insertdb.html', result=selectedrows, lastrowid=result)
        elif (sqltype == 'findvalue' or sqltype == 'findvalue_rtc' or sqltype == 'findvalue_rtc_id') :
            return "Found value is %d." % result
        elif (sqltype == 'insertvalue') :
            return "insert value finished. "

    else :
        return "Check your request..."

@app.route('/pi')
def pi():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    cpu_temperature = get_cpu_temperature()
    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    mem = psutil.virtual_memory()
    mem_total = mem.total
    mem_percent = mem.percent
    disk = psutil.disk_usage("/")
    disk_percent = disk.percent

    raspi_dict = {'CPU Temp (C)' : cpu_temperature,
            'CPU Usage (%) ' : cpu_percent,
            'CPU Core' : cpu_count,
            'Total Memory' : mem_total,
            'RAM Usage (%)' : mem_percent,
            'Disk Usage (%)' : disk_percent,
            }
    return render_template('hello.html', raspi_info = raspi_dict,
          title = 'Raspi Status',
          time = timeString)
    
@app.route('/firebase', methods=['GET'])
def firebase_database():
    action = request.args.get("action")
    duckbase.patch('/raspberrypi', {'fire' : action})
    
    message_title = request.args.get("title")
    message_body = request.args.get("body")
    result = fcm_datapush(message_title, message_body) 
    print(result)


    # firebase patch query can change a single data
    # data = { 'deeplearning' : action }
    # sionbase.put('','put', data)
    # fb.put takes three arguments : first is url or path,
    # second is the keyname or the snapshot name and
    # third is the data(json)

    print(action)
    return (''), 204

@app.errorhandler(404)
def page_not_found(error):
    return 'page_not_found_error(404)'

@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('start.html')

@app.route('/loginSuccess', methods=['POST','GET'])
def login_result():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        if user_id == 'fly' and user_pw == 'moon' :
            return render_template("loginSuccess.html", user_id = user_id)
        else :
            return render_template("again.html")


# app run
if __name__ == '__main__':
    binarysearch.weather_now()
    app.run(debug=False, host='0.0.0.0', port=11066)

    
