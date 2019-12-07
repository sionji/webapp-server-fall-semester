from firebase import firebase
from pyfcm import FCMNotification
import json

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
    global fire_pistatus, maze_i, maze_j
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

    f = open ("./info/fireinfo.txt", "w")
    data = "fire=%d\nx=%d\ny=%d"%(fire_pistatus, maze_i, maze_j)
    f.write (data)
    f.close ()

def read_fire_info () :
    global fire_pistatus, maze_i, maze_j
    with open ("./info/fireinfo.txt", "r") as file :
        line = None
        line = file.readline ()
        line = line.strip ('\n')
        fire = int (line[5:])
        line = file.readline ()
        line = line.strip ('\n')
        x = int (line[2:])
        line = file.readline ()
        line = line.strip ('\n')
        y = int (line[2:])
        fire_pistatus = fire
        maze_i = x
        maze_j = y

def get_fire_now () :
    global maze_i, maze_j
    read_fire_info ()
    return maze_i, maze_j

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


